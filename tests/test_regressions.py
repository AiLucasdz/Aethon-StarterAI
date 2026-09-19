import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]


class Regression(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = dict(os.environ, HERMES_HOME=str(self.root/'runtime'), VAULT_PATH=str(self.root/'vault'))

    def run_script(self, name, *args, ok=True):
        r = subprocess.run(['python3', str(BASE/'scripts'/name), *args], env=self.env, capture_output=True, text=True)
        if ok:
            self.assertEqual(r.returncode, 0, r.stderr+r.stdout)
        else:
            self.assertNotEqual(r.returncode, 0, r.stdout)
        return r

    def test_onboarding_preservation_skip_order_and_completion(self):
        self.run_script('iniciar.py')
        soul = self.root/'runtime/SOUL.md'
        self.assertIn('gateway_hook.py', soul.read_text())
        profile = self.root/'vault/01_IDENTIDADE/perfil.md'
        before = profile.read_bytes()
        self.run_script('iniciar.py')
        self.assertEqual(before, profile.read_bytes())
        self.run_script('onboarding.py', '--pular', 'github_token', ok=False)
        self.run_script('onboarding.py', '--responder', 'dono_nome', 'Exemplo', ok=False)
        for key, answer in [('nome','Estrela'), ('dono_nome','Pessoa fictícia'), ('dono_faz','Estudo'),
                            ('dono_desejos','Organização'), ('dono_limites','pular'), ('estilo','curtas')]:
            self.run_script('gateway_hook.py','--responder',key,answer)
        self.run_script('onboarding.py','--responder','fuso','invalido',ok=False)
        self.run_script('onboarding.py','--responder','fuso','UTC')
        self.run_script('gateway_hook.py','--pular','bot_telegram')
        self.run_script('gateway_hook.py','--responder','github_token','ghp_'+'x'*30,ok=False)
        r=self.run_script('gateway_hook.py','--responder','github_token','sim')
        self.assertIn('ONBOARDING_CONCLUIDO',r.stdout)
        self.assertIn('não configurado',r.stdout)
        self.assertNotIn('{{',soul.read_text())
        self.assertNotIn('onboarding-aethon',soul.read_text())
        self.assertEqual(soul.stat().st_mode & 0o777,0o600)
        soul.write_text(soul.read_text()+'\nPersonalização posterior\n')
        before=soul.read_bytes()
        self.run_script('iniciar.py')
        self.assertEqual(before,soul.read_bytes())

    def test_partial_vault_preserved_and_date_rejected(self):
        p=self.root/'vault/01_IDENTIDADE/perfil.md';p.parent.mkdir(parents=True);p.write_text('não sobrescrever')
        self.run_script('iniciar.py')
        self.assertEqual(p.read_text(),'não sobrescrever')
        self.run_script('diario_registrar.py','--origem','teste','--texto','fictício','--data','../../escape',ok=False)

    def test_capture_exact_id_and_dedup(self):
        for identity in ['10','1','10']:
            self.run_script('raw_capture.py','--origem','teste','--texto','fictício','--message-id',identity)
        text=(self.root/'vault/00_INBOX/para-processar.md').read_text()
        self.assertEqual(text.count('fictício'),2)

    def test_symlink_rejected(self):
        elsewhere=self.root/'elsewhere';elsewhere.mkdir()
        (self.root/'runtime').symlink_to(elsewhere,target_is_directory=True)
        self.run_script('iniciar.py',ok=False)
        self.assertEqual(list(elsewhere.iterdir()),[])


if __name__ == '__main__':
    unittest.main()

class UpdateRegression(unittest.TestCase):
    def test_fast_forward_backup_and_divergence(self):
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); upstream=root/'upstream'; fork=root/'fork'
            env=dict(os.environ, GIT_AUTHOR_NAME='Fixture',GIT_AUTHOR_EMAIL='fixture@example.invalid',
                     GIT_COMMITTER_NAME='Fixture',GIT_COMMITTER_EMAIL='fixture@example.invalid',
                     XDG_STATE_HOME=str(root/'state'))
            def git(cwd,*args):
                r=subprocess.run(['git',*args],cwd=cwd,env=env,capture_output=True,text=True)
                self.assertEqual(r.returncode,0,r.stderr)
                return r.stdout.strip()
            upstream.mkdir();git(upstream,'init','-b','main')
            (upstream/'scripts').mkdir();shutil.copyfile(BASE/'scripts/update.sh',upstream/'scripts/update.sh')
            git(upstream,'add','.');git(upstream,'commit','-m','fixture initial')
            git(root,'clone',str(upstream),str(fork));git(fork,'remote','add','upstream',str(upstream))
            (upstream/'feature').write_text('v2');git(upstream,'add','.');git(upstream,'commit','-m','fixture next')
            cmd=['bash',str(fork/'scripts/update.sh')]
            r=subprocess.run(cmd,cwd=fork,env=env,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertEqual((fork/'feature').read_text(),'v2')
            self.assertTrue(list((root/'state/aethon/base-backups').glob('*.bundle')))
            (fork/'custom').write_text('keep');git(fork,'add','.');git(fork,'commit','-m','custom')
            before=git(fork,'rev-parse','HEAD')
            (upstream/'feature').write_text('v3');git(upstream,'add','.');git(upstream,'commit','-m','fixture divergence')
            r=subprocess.run(cmd,cwd=fork,env=env,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertEqual(git(fork,'rev-parse','HEAD'),before)
            self.assertEqual((fork/'custom').read_text(),'keep')
