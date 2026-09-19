#!/usr/bin/env python3
"""Migra somente a base gerenciada do SOUL e o estado do template, com reversão."""
import argparse
import base64
import hashlib
import json
import os
import re
import shlex
import sys
import uuid
from pathlib import Path

from private_state import BASE, atomic, home, locked, read, safe, write

START = '<!-- aethon-base -->'
END = '<!-- /aethon-base -->'
TARGETS = ('SOUL.md', 'state/modulos.json', 'state/aethon-version.json')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def content(path):
    path = safe(path)
    return path.read_bytes() if path.exists() else None


def pack(data):
    return None if data is None else base64.b64encode(data).decode('ascii')


def unpack(data):
    return None if data is None else base64.b64decode(data, validate=True)


def save_bytes(path, data):
    path = safe(path)
    if data is None:
        path.unlink(missing_ok=True)
    else:
        atomic(path, data)


def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()


def managed(text):
    if START not in text and END not in text:
        return None
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('Marcadores da base ambíguos; revisão manual necessária.')
    start = text.index(START)
    end = text.index(END)
    if end < start:
        raise ValueError('Marcadores da base fora de ordem.')
    return text[start:end + len(END)]


def apply():
    root = home()
    archive = safe(root / 'state/aethon-migrations')
    if archive.exists():
        for file in archive.glob('*.json'):
            if read(file)['status'] == 'pending':
                raise ValueError(f'Migração interrompida; reverta primeiro: {file.stem}')
    before = {name: content(root / name) for name in TARGETS}
    if before['SOUL.md'] is None:
        raise ValueError('Inicialize os templates antes de migrar.')
    version = json.loads(before['state/aethon-version.json'] or '{}')
    if version.get('schema', 1) != 1:
        raise ValueError('Versão mais nova não suportada; não será rebaixada.')
    text = before['SOUL.md'].decode()
    old_block = managed(text)
    if old_block is not None and digest(old_block.encode()) != version.get('managed_sha256'):
        raise ValueError('Bloco gerenciado alterado localmente; revise antes de migrar.')
    if old_block is None and version.get('managed_sha256'):
        raise ValueError('Bloco gerenciado removido localmente; revise antes de migrar.')
    command = shlex.join(['env', f'HERMES_HOME={root}', sys.executable,
                         str(BASE / 'scripts/modulos.py')])
    vault = safe(os.environ.get('VAULT_PATH', version.get('vault', str(Path.home() / 'vault'))))
    body = (BASE / 'agent/base-operacional.md').read_text()
    for key, value in {
        '{{COMANDO_MODULOS}}': f'`{command}`', '{{VAULT_PATH}}': str(vault),
        '{{VAULT_AGENTS}}': str(vault / 'AGENTS.md'),
        '{{MEMORY_RULES}}': str(BASE / 'agent/memoria.md'),
        '{{BRAIN_GUIDE}}': str(BASE / 'docs/segundo-cerebro.md'),
    }.items():
        body = body.replace(key, value)
    onboarding = read(root / 'state/onboarding.json', {})
    fields = {k: onboarding[k] for k in ('nome', 'dono_nome', 'dono_faz', 'dono_desejos',
              'dono_limites', 'estilo', 'fuso') if onboarding.get(k) not in (None, '', '(pulado)')}
    if fields:
        body += ('\n## Escolhas do onboarding\n\n'
                 'Dados informados pelo dono: nome e estilo escolhidos substituem padrões '
                 'anteriores do agente; preserve demais personalizações e limites. '
                 'Campos ausentes não revogam escolhas anteriores.\n'
                 + json.dumps(fields, ensure_ascii=False).replace('<', '\\u003c') + '\n')
    block = START + '\n' + body.rstrip() + '\n' + END
    new_text = text.replace(old_block, block) if old_block else text + '\n' + block + '\n'
    modules = json.loads(before['state/modulos.json'] or
                         '{"schema":1,"conexoes":{},"rotinas":{}}')
    if modules.get('schema') != 1:
        raise ValueError('Schema de módulos incompatível.')
    after = {
        'SOUL.md': new_text.encode(),
        'state/modulos.json': before['state/modulos.json'] or encoded(modules),
        'state/aethon-version.json': encoded({'schema': 1, 'managed_sha256': digest(block.encode()), 'vault': str(vault)}),
    }
    if before == after:
        print('Base privada já atualizada; personalizações preservadas.')
        return
    identity = uuid.uuid4().hex
    path = safe(archive / (identity + '.json'))
    journal = {'status': 'pending', 'before': {k: pack(v) for k, v in before.items()},
               'after': {k: pack(v) for k, v in after.items()}}
    write(path, journal)
    if read(path) != journal:
        raise ValueError('Backup não passou na verificação; nada aplicado.')
    try:
        for name, data in after.items():
            save_bytes(root / name, data)
        journal['status'] = 'applied'
        write(path, journal)
    except Exception:
        for name, data in before.items():
            save_bytes(root / name, data)
        journal['status'] = 'rolled_back'
        write(path, journal)
        raise
    print(f'Migração aplicada. Reversão: python3 scripts/migrar.py --rollback {identity}')
    print('Backup privado verificado apenas dos arquivos migrados; não é backup completo do runtime.')


def rollback(identity):
    if not re.fullmatch('[a-f0-9]{32}', identity):
        raise ValueError('Identificador de migração inválido.')
    root = home()
    path = safe(root / 'state/aethon-migrations' / (identity + '.json'))
    journal = read(path)
    if not journal:
        raise ValueError('Migração não encontrada.')
    if journal['status'] == 'rolled_back':
        print('Migração já revertida.')
        return
    if set(journal['before']) != set(TARGETS) or set(journal['after']) != set(TARGETS):
        raise ValueError('Manifesto de backup inválido.')
    before = {k: unpack(v) for k, v in journal['before'].items()}
    after = {k: unpack(v) for k, v in journal['after'].items()}
    for name in TARGETS:
        if content(root / name) not in (before[name], after[name]):
            raise ValueError(f'{name} mudou após migração; reversão recusada para preservar mudanças.')
    # Pending permite retomar a reversão após uma interrupção do processo.
    journal['status'] = 'pending'
    write(path, journal)
    for name, data in before.items():
        save_bytes(root / name, data)
    journal['status'] = 'rolled_back'
    write(path, journal)
    print('Migração revertida; conteúdo anterior restaurado.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument('--apply', action='store_true')
    actions.add_argument('--rollback')
    actions.add_argument('--status', action='store_true')
    args = parser.parse_args()
    with locked():
        if args.apply:
            apply()
        elif args.rollback:
            rollback(args.rollback)
        else:
            print(json.dumps(read(home() / 'state/aethon-version.json', {'schema': 0}), indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print(f'ERRO: {error}', file=sys.stderr)
        raise SystemExit(1)
