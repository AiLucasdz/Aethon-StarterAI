"""Um proprietário PGLite por perfil; transporte HTTP nativo, somente loopback."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import time
import urllib.request
import uuid

from private_state import atomic, read, safe, write


def systemctl(*args):
    result = subprocess.run(['systemctl', '--user', *args], capture_output=True,
                            text=True, timeout=45)
    if result.returncode:
        raise RuntimeError('systemd de usuário indisponível ou serviço falhou; GBrain pendente. '
                           'Consulte docs/gbrain-runtime.md; não iniciar outro servidor stdio.')
    return result.stdout


def quote(value):
    value = str(value)
    if any(c in value for c in '\n\r\0'):
        raise ValueError('Caminho inválido para unidade systemd')
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"').replace('%', '%%') + '"'


def wait_ready(url):
    for _ in range(60):
        try:
            with urllib.request.urlopen(url.replace('/mcp', '/health'), timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            pass
        time.sleep(.5)
    raise RuntimeError('GBrain não ficou saudável; consulte o journal da unidade no recibo privado.')


def install(root, vault, brain, brain_home, brain_env):
    """Retoma instalação parcial sem reabrir um banco já servido. Não migra bancos alheios."""
    systemctl('show-environment')  # Falhar antes de modificar o banco quando não há supervisor.
    name = 'aethon-gbrain-' + hashlib.sha256(str(root).encode()).hexdigest()[:12] + '.service'
    receipt_path = root / 'state/aethon-memory/gbrain-service.json'
    receipt = read(receipt_path)
    if receipt:
        if receipt.get('unit') != name or receipt.get('brain_home') != str(brain_home):
            raise RuntimeError('Recibo de outro perfil: não conectar nem modificar a base original.')
        systemctl('enable', '--now', receipt['unit'])
        wait_ready(receipt['server']['url'])
        return receipt['server']
    bun = shutil.which('bun')
    if not bun:
        raise RuntimeError('Bun ausente; necessário para executar o serviço GBrain.')
    units = safe(Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'systemd/user')
    unit = safe(units / name)
    if unit.exists():
        raise RuntimeError('Unidade sem recibo correspondente; revisar instalação parcial antes de continuar.')
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]

    def run(*args):
        result = subprocess.run([brain, *args], env=brain_env, cwd=vault,
                                capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise RuntimeError(f'GBrain falhou em {args[0]}; dados preservados, saída privada não exibida.')
        return result.stdout

    if not (brain_home / '.gbrain/config.json').exists():
        run('init', '--pglite', '--non-interactive', '--no-embedding')
        run('config', 'set', 'search.mode', 'conservative')
    run('import', str(vault), '--no-embed')
    output = run('auth', 'create', 'hermes-' + uuid.uuid4().hex[:12], '--scopes', 'read,write')
    match = re.search(r'gbrain_[a-f0-9]{64}', output)
    if not match:
        raise RuntimeError('GBrain não retornou token MCP; configuração não aplicada.')
    # Referência por variável: segredo nunca passa como argumento de config set.
    variable = 'AETHON_GBRAIN_TOKEN_' + uuid.uuid4().hex[:12].upper()
    dotenv = safe(root / '.env')
    previous = dotenv.read_bytes() if dotenv.exists() else b''
    atomic(dotenv, previous + ('\n' + variable + '=' + match.group(0) + '\n').encode())
    url = f'http://127.0.0.1:{port}/mcp'
    server = {'url': url, 'headers': {'Authorization': 'Bearer ${' + variable + '}'},
              'enabled': True, 'connect_timeout': 60}
    contents = ('[Unit]\nDescription=GBrain shared local memory\nStartLimitIntervalSec=60\nStartLimitBurst=5\n'
                '[Service]\nType=simple\nEnvironment=' + quote('GBRAIN_HOME=' + str(brain_home)) + '\n'
                'ExecStart=' + quote(bun).replace('$', '$$') + ' ' + quote(brain).replace('$', '$$') +
                f' serve --http --bind 127.0.0.1 --port {port} --surface verbs --no-print-admin-token\n'
                'Restart=always\nRestartSec=5\nKillMode=control-group\nTimeoutStopSec=30\nUMask=0077\n'
                '[Install]\nWantedBy=default.target\n')
    atomic(unit, contents.encode())
    # Receipt before startup: a retry never opens PGLite from a second process.
    write(receipt_path, {'unit': name, 'unit_path': str(unit), 'server': server,
                         'brain_home': str(brain_home)})
    systemctl('daemon-reload')
    systemctl('enable', '--now', name)
    wait_ready(url)
    return server
