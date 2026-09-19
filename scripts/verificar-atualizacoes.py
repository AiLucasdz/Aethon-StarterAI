#!/usr/bin/env python3
"""Consulta semanal sem LLM; stdout vazio quando não há atualização pendente."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

UPSTREAM = 'https://github.com/AiLucasdz/Aethon-StarterAI.git'


def check(repo, remote=UPSTREAM, branch='main'):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0')

    def git(*args, allowed=(0,)):
        result = subprocess.run(['git', '-C', str(repo), *args], env=env,
                                capture_output=True, text=True, timeout=90)
        if result.returncode not in allowed:
            # Não reproduzir URL/credencial nem stderr arbitrário no Telegram.
            raise RuntimeError('Consulta do template falhou; confira rede e checkout.')
        return result

    head = git('rev-parse', 'HEAD').stdout.strip()
    # Atualiza somente referências Git; não faz checkout, merge ou migração.
    git('fetch', '--quiet', '--no-tags', '--no-recurse-submodules', remote,
        'refs/heads/' + branch)
    latest = git('rev-parse', 'FETCH_HEAD').stdout.strip()
    if git('merge-base', '--is-ancestor', latest, head, allowed=(0, 1)).returncode == 0:
        return ''
    return (f'Há atualização pendente do template ({latest[:7]}). '
            'Para revisar e aplicar preservando suas personalizações, diga: '
            '“Verifique e atualize meu agente pelo template”. '
            'Nenhuma atualização foi aplicada automaticamente.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        message = check(args.repo)
    except (OSError, RuntimeError, subprocess.TimeoutExpired):
        print('Não foi possível consultar o template; confira o checkout e a rede.', file=sys.stderr)
        return 1
    if message:
        print(message)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
