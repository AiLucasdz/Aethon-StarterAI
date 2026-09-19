#!/usr/bin/env python3
"""Instala GBrain/recuperação e configura Honcho quando aceito, preservando o modelo."""
import argparse
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import uuid

from private_state import BASE, atomic, home, locked, read, safe, write


def configurar_honcho(binary, root, env, choice):
    """Etapa da instalação; recusa não altera provider nem credenciais existentes."""
    if choice != 'solicitado':
        return {'estado': 'recusado' if choice == '(pulado)' else 'aguardando_escolha'}
    current = subprocess.run([binary, 'config', 'get', 'memory.provider', '--json'],
                             env=env, capture_output=True, text=True, timeout=45)
    if current.returncode:
        if 'Config key not set: memory.provider' not in current.stdout + current.stderr:
            raise RuntimeError('Não foi possível conferir o provider; Honcho pendente, sem sobrescrever configuração.')
        provider = None
    else:
        provider = json.loads(current.stdout)
    if provider == 'honcho':
        return {'estado': 'existente_validacao_pendente'}
    if provider not in (None, '', 'none', 'local'):
        return {'estado': 'conflito_provider', 'acao': 'Revisar troca do provider existente com o dono.'}
    command = [binary, 'memory', 'setup', 'honcho']
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return {'estado': 'autenticacao_pendente', 'comando_terminal': shlex.join(
            ['env', f'HERMES_HOME={root}', *command])}
    # Wizard nativo: OAuth/device code ou entrada protegida, sem chaves em argv.
    result = subprocess.run(command, env=env, timeout=900)
    if result.returncode:
        return {'estado': 'setup_incompleto'}
    after = subprocess.run([binary, 'config', 'get', 'memory.provider', '--json'],
                           env=env, capture_output=True, text=True, timeout=45)
    enabled = after.returncode == 0 and json.loads(after.stdout) == 'honcho'
    return {'estado': 'configurado_validacao_pendente' if enabled else 'setup_incompleto'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hermes', default='hermes', help='Executável do Hermes deste perfil')
    parser.add_argument('--telegram-owner', help='ID numérico do dono confirmado no DM, não username')
    parser.add_argument('--gbrain-bin', default='gbrain', help='Executável existente; se ausente instala via Bun/GitHub')
    args = parser.parse_args()
    if args.telegram_owner and not args.telegram_owner.isdecimal():
        parser.error('Use o ID numérico do remetente confirmado no DM.')
    binary = shutil.which(args.hermes)
    if not binary:
        parser.error('Hermes não encontrado; SOUL/vault podem ser usados sem o plugin.')
    root = home()
    vault = safe(os.environ.get('VAULT_PATH', Path.home() / 'vault'))
    if not (vault / 'AGENTS.md').is_file():
        parser.error('Inicialize o vault primeiro com iniciar.py.')
    env = dict(os.environ, HERMES_HOME=str(root))

    def run(*arguments):
        result = subprocess.run([binary, *arguments], env=env, capture_output=True, text=True, timeout=45)
        if result.returncode:
            if arguments == ('config', 'get', 'mcp_servers', '--json') and 'Config key not set: mcp_servers' in result.stdout + result.stderr:
                return '{}'
            # Config pode conter segredos: não reproduzir stdout/stderr do CLI.
            raise RuntimeError(f'Hermes falhou em {arguments[0]} (exit {result.returncode}); confira compatibilidade/configuração local.')
        return result.stdout

    if str(root / 'config.yaml') not in run('config', 'path'):
        parser.error('Hermes não confirmou o perfil solicitado; nenhuma ativação aplicada.')
    with locked():
        config = safe(root / 'config.yaml')
        previous = config.read_bytes()
        folder = safe(root / 'plugins')
        folder.mkdir(exist_ok=True)
        target = folder / 'aethon-memory'
        source = BASE / 'plugins/aethon-memory'
        existing = target.is_symlink() and target.resolve() == source.resolve()
        if (target.exists() or target.is_symlink()) and not existing:
            parser.error('Plugin existente de outra origem; não sobrescrito.')
        backup = root / 'state/aethon-memory' / f'config-{uuid.uuid4().hex}.yaml'
        atomic(backup, previous)
        try:
            if not existing:
                target.symlink_to(source, target_is_directory=True)
            servers = json.loads(run('config', 'get', 'mcp_servers', '--json')) or {}
            if 'gbrain' not in servers:
                brain = shutil.which(args.gbrain_bin)
                if not brain:
                    bun = shutil.which('bun')
                    if not bun:
                        raise RuntimeError('Bun ausente. Instale pelo guia oficial e retome este comando; GBrain pendente.')
                    subprocess.run([bun, 'install', '-g', 'github:garrytan/gbrain#v0.46.12.3'], check=True, timeout=300)
                    brain = shutil.which(args.gbrain_bin) or str(Path(bun).parent / 'gbrain')
                brain_home = safe(root.with_name(root.name + '-gbrain'))
                # Não herdar overrides de outro cérebro/perfil.
                brain_env = {k: v for k, v in env.items() if not k.startswith('GBRAIN_')}
                brain_env['GBRAIN_HOME'] = str(brain_home)
                def gbrain(*arguments):
                    result = subprocess.run([brain, *arguments], env=brain_env, cwd=vault,
                                            capture_output=True, text=True, timeout=120)
                    if result.returncode:
                        raise RuntimeError(f'GBrain falhou em {arguments[0]}; configuração incompleta, dados preservados.')
                if not (brain_home / '.gbrain/config.json').exists():
                    gbrain('init', '--pglite', '--non-interactive', '--no-embedding')
                    gbrain('config', 'set', 'search.mode', 'conservative')
                gbrain('import', str(vault), '--no-embed')
                server = {'command': brain, 'args': ['serve', '--surface', 'verbs'],
                          'env': {'GBRAIN_HOME': str(brain_home)}, 'enabled': True,
                          'connect_timeout': 60}
                run('config', 'set', 'mcp_servers.gbrain', json.dumps(server))
            elif servers['gbrain'].get('enabled') is False:
                raise RuntimeError('GBrain existente desativado: revisar o motivo antes de reativar. Configuração preservada.')
            key = 'plugins.entries.aethon-memory.'
            for name, value in [('settings.home', str(root)), ('settings.vault', str(vault))]:
                run('config', 'set', key + name, value)
            if args.telegram_owner:
                run('config', 'set', key + 'settings.owner_id', args.telegram_owner)
            run('config', 'set', key + 'mcp_allowlist', '["gbrain"]')
            run('config', 'set', key + 'settings.gbrain_enabled', 'true')
            run('plugins', 'enable', 'aethon-memory', '--no-allow-tool-override')
        except Exception:
            atomic(config, previous)
            if not existing and target.is_symlink():
                target.unlink()
            raise
        print(f'Recuperação instalada neste perfil. Backup privado: {backup}')
        print('Recarregue o gateway fora do turno ativo e valide uma nova sessão.')
        print('Telegram exige owner_id configurado e DM confirmado; grupos não recebem contexto privado.')
        print('GBrain incluído: base nova começa sem embeddings/API; configuração existente é preservada.')
        print('Valide remember/recall pelo MCP do agente. Cadastro não comprova conexão nem busca semântica.')
    # Fora do lock: autenticação pode aguardar interação do dono.
    onboarding = read(root / 'state/onboarding.json', {})
    choice = onboarding.get('honcho', onboarding.get('segundo_cerebro'))
    honcho = configurar_honcho(binary, root, env, choice)
    with locked():
        write(root / 'state/aethon-memory/honcho.json', honcho)
    print('Honcho: ' + honcho['estado'])
    if honcho.get('comando_terminal'):
        print('Continue a etapa de autenticação no terminal seguro: ' + honcho['comando_terminal'])
        print('O agente pode conduzir OAuth/device code por PTY e mostrar o link; nunca pedir API key no chat.')
    if honcho.get('acao'):
        print(honcho['acao'])
    print('Só confirmar Honcho após verificar identidade, contexto no consumidor e gravações separadamente.')


if __name__ == '__main__':
    main()
