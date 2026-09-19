"""Ciclo isolado com pessoa fictícia; nenhuma conta ou API externa."""
import base64
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]


class Lifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='aethon-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.checkout = self.root / 'checkout'
        shutil.copytree(BASE, self.checkout, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        self.home = self.root / 'runtime'
        self.env = dict(os.environ, HERMES_HOME=str(self.home), VAULT_PATH=str(self.root / 'vault'))

    def run_script(self, name, *args, ok=True):
        result = subprocess.run(['python3', str(self.checkout / 'scripts' / name), *args],
                                env=self.env, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def journals(self):
        return list((self.home / 'state/aethon-migrations').glob('*.json'))

    def test_installer_arguments_never_modify_private_files(self):
        self.home.mkdir()
        soul = self.home / 'SOUL.md'
        soul.write_text('Existing private identity\n')
        before = soul.read_bytes()
        self.run_script('iniciar.py', '--help')
        self.run_script('iniciar.py', '--unknown-option', ok=False)
        self.assertEqual(soul.read_bytes(), before)
        self.assertEqual(list(self.home.iterdir()), [soul])
        self.assertFalse((self.root / 'vault').exists())

    def test_full_install_resume_choices_update_rollback(self):
        self.home.mkdir()
        config = self.home / 'config.yaml'
        config.write_text('custom: keep\n')
        self.run_script('iniciar.py')
        soul = self.home / 'SOUL.md'
        self.assertIn('aethon-base', soul.read_text())
        self.assertEqual(len(self.journals()), 1)
        self.run_script('iniciar.py')
        self.assertEqual(len(self.journals()), 1)
        self.run_script('gateway_hook.py', '--responder', 'nome', 'Aurora')
        self.assertIn('apresentacao', self.run_script('gateway_hook.py').stdout)
        for key in ['apresentacao', 'honcho']:
            result = self.run_script('gateway_hook.py', '--pular', key)
        self.assertIn('ONBOARDING_CONCLUIDO', result.stdout)
        self.assertIn('Aurora', soul.read_text())
        self.assertNotIn('{{', soul.read_text())
        self.run_script('modulos.py', 'solicitar', 'conexao', 'google-tasks')
        self.run_script('modulos.py', 'solicitar', 'rotina', 'regar-plantas')
        self.run_script('modulos.py', 'desativar', 'conexao', 'youtube')
        modules_path = self.home / 'state/modulos.json'
        choices = modules_path.read_bytes()
        state = json.loads(choices)
        self.assertNotIn('google-agenda', state['conexoes'])
        self.assertEqual(state['rotinas']['regar-plantas']['desejado'], 'solicitado')
        self.assertEqual(state['conexoes']['youtube']['desejado'], 'desativado')
        soul.write_text(soul.read_text() + '\nMinha preferência fictícia: respostas breves.\n')
        before = soul.read_bytes()
        base = self.checkout / 'agent/base-operacional.md'
        base.write_text(base.read_text() + '\nMelhoria de teste.\n')
        prior = set(self.journals())
        self.run_script('migrar.py', '--apply')
        self.assertIn('Melhoria de teste.', soul.read_text())
        self.assertIn('Minha preferência fictícia', soul.read_text())
        self.assertEqual(modules_path.read_bytes(), choices)
        self.assertEqual(config.read_text(), 'custom: keep\n')
        snapshot = (set(self.journals()) - prior).pop()
        self.assertEqual(snapshot.stat().st_mode & 0o777, 0o600)
        self.run_script('migrar.py', '--rollback', snapshot.stem)
        self.assertEqual(soul.read_bytes(), before)
        self.run_script('migrar.py', '--rollback', snapshot.stem)

    def test_conflicts_and_future_versions_preserve_data(self):
        self.run_script('iniciar.py')
        soul = self.home / 'SOUL.md'
        soul.write_text(soul.read_text().replace('## Padrão inicial', '## Meu padrão'))
        before = soul.read_bytes()
        self.run_script('migrar.py', '--apply', ok=False)
        self.run_script('migrar.py', '--rollback', self.journals()[0].stem, ok=False)
        self.assertEqual(soul.read_bytes(), before)
        modules = self.home / 'state/modulos.json'
        modules.write_text('{"schema":999}')
        self.run_script('modulos.py', 'solicitar', 'rotina', 'teste', ok=False)
        self.assertEqual(modules.read_text(), '{"schema":999}')

    def test_existing_identity_and_honcho_refusal_keep_gbrain(self):
        self.home.mkdir()
        (self.home / 'SOUL.md').write_text('# Hermes\nPreferência fictícia preservada.\n')
        self.run_script('iniciar.py')
        self.run_script('gateway_hook.py', '--responder', 'nome', 'Aurora')
        for key in ['apresentacao', 'honcho']:
            self.run_script('gateway_hook.py', '--pular', key)
        soul = (self.home / 'SOUL.md').read_text()
        self.assertIn('Aurora', soul)
        self.assertIn('Preferência fictícia preservada.', soul)
        self.assertIn(str(self.root / 'vault' / 'AGENTS.md'), soul)
        modules = json.loads((self.home / 'state/modulos.json').read_text())
        self.assertEqual(modules['conexoes']['gbrain']['desejado'], 'solicitado')
        self.assertEqual(modules['conexoes']['honcho']['desejado'], 'desativado')

    def test_honcho_acceptance_does_not_deadlock_and_old_state_resumes(self):
        self.run_script('iniciar.py')
        state = self.home / 'state/onboarding.json'
        state.write_text(json.dumps({k: '(pulado)' for k in ['nome', 'dono_nome',
            'dono_faz', 'dono_desejos', 'dono_limites', 'estilo', 'fuso', 'bot_telegram', 'github_token']}))
        self.run_script('gateway_hook.py', '--responder', 'honcho', 'sim')
        modules = json.loads((self.home / 'state/modulos.json').read_text())
        self.assertEqual(modules['conexoes']['honcho']['desejado'], 'solicitado')
        old = json.loads(state.read_text())
        old['segundo_cerebro'] = old.pop('honcho')
        state.write_text(json.dumps(old))
        self.assertIn('ONBOARDING_CONCLUIDO', self.run_script('gateway_hook.py').stdout)

    def test_plugin_activation_failure_restores_config_and_preserves_existing_mcp(self):
        self.run_script('iniciar.py')
        config = self.home / 'config.yaml'
        before = b'custom: preserve\n'
        config.write_bytes(before)
        fake = self.root / 'hermes-fixture'
        fake.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
p = Path(os.environ['HERMES_HOME']) / 'config.yaml'
args = sys.argv[1:]
if args == ['config', 'path']:
    print(p)
elif args == ['config', 'get', 'mcp_servers', '--json']:
    print(json.dumps({'gbrain': {'command': 'existing-server', 'enabled': True}}))
elif args[:2] == ['config', 'set']:
    assert args[2] != 'mcp_servers.gbrain', 'Não substituir servidor existente'
    p.write_text(p.read_text() + '# alteração parcial fictícia\\n')
elif args[:2] == ['plugins', 'enable']:
    raise SystemExit(1)
else:
    raise SystemExit(2)
''')
        fake.chmod(0o700)
        self.run_script('ativar-memoria.py', '--hermes', str(fake), '--gbrain-bin', '/nao-existe', ok=False)
        self.assertEqual(config.read_bytes(), before)
        self.assertFalse((self.home / 'plugins/aethon-memory').is_symlink())
        backups = list((self.home / 'state/aethon-memory').glob('config-*.yaml'))
        self.assertEqual(backups[0].read_bytes(), before)
        self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)

    def test_interrupted_migration_recovery(self):
        self.run_script('iniciar.py')
        snapshot = self.journals()[0]
        journal = json.loads(snapshot.read_text())
        journal['status'] = 'pending'
        snapshot.write_text(json.dumps(journal))
        # Simula interrupção depois da primeira escrita: outros arquivos ausentes.
        (self.home / 'state/modulos.json').unlink()
        (self.home / 'state/aethon-version.json').unlink()
        self.run_script('migrar.py', '--apply', ok=False)
        self.run_script('migrar.py', '--rollback', snapshot.stem)
        self.assertEqual((self.home / 'SOUL.md').read_bytes(),
                         base64.b64decode(journal['before']['SOUL.md']))
        self.run_script('migrar.py', '--apply')

    def test_private_paths_and_traversal_rejected(self):
        self.run_script('iniciar.py')
        self.run_script('modulos.py', 'solicitar', 'rotina', '../../escape', ok=False)
        self.run_script('migrar.py', '--rollback', '../../escape', ok=False)
        modules = self.home / 'state/modulos.json'
        modules.unlink()
        outside = self.root / 'outside.json'
        outside.write_text('keep')
        modules.symlink_to(outside)
        self.run_script('modulos.py', 'solicitar', 'conexao', 'teste', ok=False)
        self.run_script('migrar.py', '--apply', ok=False)
        self.assertEqual(outside.read_text(), 'keep')
        self.env['HERMES_HOME'] = str(self.checkout / 'private')
        self.run_script('modulos.py', 'listar', ok=False)
        self.assertFalse((self.checkout / 'private').exists())


if __name__ == '__main__':
    unittest.main()
