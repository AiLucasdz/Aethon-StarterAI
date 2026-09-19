#!/usr/bin/env python3
"""Teste offline com Hermes instalado e runtime fictício; nunca usa o perfil pessoal."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

BASE = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hermes', required=True, help='Executável do Hermes já instalado')
    parser.add_argument('--gbrain', help='Executável GBrain existente para teste isolado sem APIs')
    parser.add_argument('--manter', action='store_true', help='Mantém o ambiente fictício para inspeção')
    args = parser.parse_args()
    hermes = Path(args.hermes).expanduser().resolve()
    if not hermes.is_file():
        parser.error('Executável do Hermes não encontrado')
    root = Path(tempfile.mkdtemp(prefix='aethon-runtime-test-'))
    home = root / 'runtime'
    home.mkdir(mode=0o700)
    # Não herda credenciais, perfil ativo nem variáveis de integrações da sessão.
    env = {'PATH': str(hermes.parent) + os.pathsep + os.defpath,
           'LANG': 'C.UTF-8', 'HERMES_HOME': str(home),
           'VAULT_PATH': str(root / 'vault'), 'PYTHONIOENCODING': 'utf-8'}
    (home / 'config.yaml').write_text('memory:\n  provider: null\n')
    (home / 'SOUL.md').write_text('# Hermes\nIdentidade anterior fictícia.\nPersonalização a preservar.\n')
    records = []

    def run(label, command, current_env=None):
        start = time.monotonic()
        result = subprocess.run(command, env=current_env or env, cwd=root,
                                capture_output=True, text=True, timeout=60)
        records.append({'etapa': label, 'segundos': round(time.monotonic() - start, 3),
                        'exit_code': result.returncode})
        if result.returncode:
            raise RuntimeError(f'{label}: {result.stdout}\n{result.stderr}')
        return result.stdout

    def script(name, *arguments, current_env=None):
        return run(name + ' ' + ' '.join(arguments[:1]),
                   [sys.executable, str(BASE / 'scripts' / name), *arguments], current_env)

    try:
        resolved = run('config path', [str(hermes), 'config', 'path'])
        if str(home / 'config.yaml') not in resolved:
            raise RuntimeError('Hermes não confirmou o runtime isolado; teste interrompido.')
        script('iniciar.py')
        script('gateway_hook.py', '--responder', 'nome', 'Aurora')
        for key in ['apresentacao', 'honcho']:
            completion = script('gateway_hook.py', '--pular', key)
        if 'ONBOARDING_CONCLUIDO' not in completion:
            raise RuntimeError('Onboarding não concluiu; teste interrompido.')
        if '{{' in (home / 'SOUL.md').read_text():
            raise RuntimeError('SOUL ainda contém placeholders após onboarding.')
        if 'Aurora' not in (home / 'SOUL.md').read_text() or 'Personalização a preservar.' not in (home / 'SOUL.md').read_text():
            raise RuntimeError('Identidade escolhida/personalização não chegou ao SOUL existente.')
        if args.gbrain:
            # Bun precisa estar no PATH para o shebang do executável GBrain.
            brain = Path(args.gbrain).expanduser().absolute()
            env['PATH'] = str(brain.parent) + os.pathsep + env['PATH']
            script('ativar-memoria.py', '--hermes', str(hermes), '--gbrain-bin', str(brain),
                   '--telegram-owner', '123456')
            before = (home / 'config.yaml').read_bytes()
            # Repetir não abre/reimporta um servidor existente, nem muda configuração.
            script('ativar-memoria.py', '--hermes', str(hermes), '--gbrain-bin', '/fixture-nao-existe')
            if before != (home / 'config.yaml').read_bytes():
                raise RuntimeError('Reativação mudou configuração existente.')
            run('consumidor nativo de memória', [str(hermes.parent / 'python'),
                str(BASE / 'tests/native_memory_probe.py')])
        script('modulos.py', 'solicitar', 'rotina', 'regar-plantas')
        run('perfil opcional', ['bash', str(BASE / 'scripts/configurar_hermes.sh'), '--perfil-leve'])
        threshold = run('threshold efetivo', [str(hermes), 'config', 'get',
                                             'compression.threshold_tokens', '--json'])
        if json.loads(threshold) != 300000:
            raise RuntimeError('Hermes não leu o threshold configurado.')
        archive = root / 'runtime.zip'
        run('backup nativo', [str(hermes), 'backup', '--output', str(archive)])
        archive.chmod(0o600)
        with zipfile.ZipFile(archive) as backup:
            if backup.testzip() is not None:
                raise RuntimeError('Backup corrompido.')
            if any('_external' in Path(name).parts for name in backup.namelist()):
                raise RuntimeError('Backup incluiu estado externo inesperado; restauração interrompida.')
        restored = root / 'restored'
        restore_env = dict(env, HERMES_HOME=str(restored))
        run('restauração nativa', [str(hermes), 'import', str(archive)], restore_env)
        for name in ['SOUL.md', 'config.yaml', 'state/modulos.json', 'state/onboarding.json']:
            if (home / name).read_bytes() != (restored / name).read_bytes():
                raise RuntimeError(f'Restauração divergente: {name}')
        script('migrar.py', '--apply', current_env=restore_env)
        report = {'resultado': 'aprovado', 'etapas': records,
                  'limites': ['Sem modelo/API, Telegram ou OAuth',
                              'Backup nativo só do runtime fictício; vault e base GBrain externos não incluídos',
                              'Tempos de CLI não representam latência de conversa ou benchmark KVM 1']}
        (root / 'resultado.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(report, ensure_ascii=False, indent=2))
    finally:
        if args.manter:
            print(f'Ambiente fictício mantido em: {root}')
        else:
            shutil.rmtree(root)


if __name__ == '__main__':
    main()
