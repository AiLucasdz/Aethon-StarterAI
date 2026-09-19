#!/usr/bin/env python3
"""Instala só os templates privados; não inicia serviços nem conecta contas."""
import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path
from private_state import safe

BASE = Path(__file__).resolve().parent.parent


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description='Instala só os templates privados; não inicia serviços nem conecta contas.')
    parser.parse_args(argv)
    return parser


def main(argv=None):
    parse_args(sys.argv[1:] if argv is None else argv)
    home = Path(os.environ.get('HERMES_HOME', Path.home() / '.hermes')).expanduser()
    vault = Path(os.environ.get('VAULT_PATH', Path.home() / 'vault')).expanduser()
    for target in (home, vault):
        if target.is_symlink() or target.resolve().is_relative_to(BASE):
            raise ValueError('Destino privado deve estar fora do checkout, sem symlink na raiz.')
        for part in [target, *target.parents]:
            if part.is_symlink():
                raise ValueError('Destino privado contém symlink; configuração manual necessária.')
    os.umask(0o077)
    for src in (BASE / 'templates/vault').rglob('*'):
        if not src.is_file():
            continue
        dst = safe(vault / src.relative_to(BASE / 'templates/vault'))
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_symlink():
            raise ValueError('Arquivo privado é symlink; recusado.')
        if not dst.exists():
            with dst.open('x') as f:
                f.write(src.read_text())
    home.mkdir(parents=True, exist_ok=True)
    soul = home / 'SOUL.md'
    if soul.is_symlink():
        raise ValueError('SOUL é symlink; recusado.')
    if not soul.exists():
        with soul.open('x') as f:
            f.write((BASE / 'templates/soul-template.md').read_text())
    env = dict(os.environ, HERMES_HOME=str(home), VAULT_PATH=str(vault))
    result = subprocess.run([sys.executable, str(BASE / 'scripts/onboarding.py'), '--iniciar'],
                            env=env, text=True, capture_output=True, check=True)
    text = soul.read_text()
    if 'ONBOARDING_CONCLUIDO' not in result.stdout and '<!-- onboarding-aethon -->' not in text:
        cmd = shlex.join(['env', f'HERMES_HOME={home}', f'VAULT_PATH={vault}', sys.executable,
                          str(BASE / 'scripts/gateway_hook.py')])
        text += ('\n<!-- onboarding-aethon -->\n## Configuração inicial pendente\n'
                 f'Antes de perguntar nome ou perfil, conclua a preparação técnica de {BASE / "docs/instalar-pelo-telegram.md"}: '
                 'GBrain e áudio local medium configurados/testados, ou impedimento técnico informado. '
                 f'Só então execute `{cmd}`. '
                 'Nome do agente, depois apresentação livre; pergunte só lacunas necessárias. '
                 f'Para organizar áudio/documento, leia {BASE / "docs/onboarding.md"}. '
                 'Use --apresentacao-json ARQUIVO_PRIVADO para perfil organizado. '
                 'Para resposta simples use --responder CHAVE RESPOSTA, '
                 'com argumentos escapados; para pular use --pular CHAVE. '
                 'Nunca passe tokens ou chaves. Se a pessoa pedir ajuda em outro assunto, ajude e retome depois. '
                 'Após ONBOARDING_CONCLUIDO não execute mais este fluxo. '
                 'Não alegue que módulos ou backups estão ativos sem teste.\n'
                 '<!-- /onboarding-aethon -->\n')
        soul.write_text(text)
    soul.chmod(0o600)
    subprocess.run([sys.executable, str(BASE / 'scripts/migrar.py'), '--apply'],
                   env=env, check=True)
    from modulos import registrar_intencao
    registrar_intencao({})
    print('Templates preservados/criados; onboarding preparado no SOUL.')
    print('Antes de perguntar nome/perfil: ativar-memoria.py e áudio medium conforme docs/midia.md. Honcho é opcional depois.')
    print('O gateway deve carregar este HERMES_HOME; novas sessões usam o SOUL atualizado.')
    print('Pareamento Telegram e configuração Hermes são pré-requisitos; não foram executados aqui.')


if __name__ == '__main__':
    main()
