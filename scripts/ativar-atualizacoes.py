#!/usr/bin/env python3
"""Instala consulta semanal no cron nativo, sem LLM e sem aplicar atualizações."""
import argparse
import json
import os
import shutil
import subprocess

from private_state import BASE, atomic, home, locked, read, safe

NAME = 'aethon-atualizacoes-semanais'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hermes', default='hermes')
    parser.add_argument('--telegram-owner', required=True, help='ID positivo do dono confirmado no DM')
    args = parser.parse_args()
    if not args.telegram_owner.isdecimal() or int(args.telegram_owner) <= 0:
        parser.error('Confirme o ID positivo do dono no DM; grupos não são destinos.')
    binary = shutil.which(args.hermes)
    if not binary:
        parser.error('Hermes não encontrado; consulta semanal pendente.')
    root = home()
    env = dict(os.environ, HERMES_HOME=str(root))

    def run(*arguments):
        result = subprocess.run([binary, *arguments], env=env, capture_output=True,
                                text=True, timeout=60)
        if result.returncode:
            raise RuntimeError('Hermes não concluiu o comando; confira compatibilidade no perfil alvo.')
        return result.stdout

    if str(root / 'config.yaml') not in run('config', 'path'):
        parser.error('Perfil alvo não confirmado; nenhum agendamento criado.')
    if '--no-agent' not in run('cron', 'create', '--help'):
        parser.error('Este Hermes não oferece cron sem LLM; consulta semanal pendente.')
    target = safe(root / 'scripts/aethon-update-check.py')
    header = '# Gerenciado por Aethon: consulta semanal, sem atualizacao automatica.\n'
    wrapper = (header + 'import runpy, sys\n'
               + f'sys.argv = [{str(BASE / "scripts/verificar-atualizacoes.py")!r}, "--repo", {str(BASE)!r}]\n'
               + f'runpy.run_path({str(BASE / "scripts/verificar-atualizacoes.py")!r}, run_name="__main__")\n')
    with locked():
        jobs_file = root / 'cron/jobs.json'

        def jobs():
            data = read(jobs_file, {'jobs': []})
            rows = data.get('jobs') if isinstance(data, dict) else None
            if not isinstance(rows, list):
                raise ValueError('Formato do cron desconhecido; estado preservado.')
            return [j for j in rows if j.get('name') == NAME]

        existing = jobs()
        if existing:
            # Reexecução não duplica, não muda destinatário nem reativa uma pausa.
            print('Agendamento existente preservado. Confira destino, script e estado pelo cron nativo.')
            print(json.dumps([{'id': j['id'], 'enabled': j.get('enabled')} for j in existing]))
            return
        if target.exists() and target.read_text() != wrapper:
            raise ValueError('Script existente diferente; revisão necessária, sem sobrescrever.')
        atomic(target, wrapper.encode())
        run('cron', 'create', 'every 7d', '--name', NAME, '--script', target.name,
            '--no-agent', '--deliver', 'telegram:' + args.telegram_owner,
            '--failure-deliver', 'local')
        created = jobs()
        if (len(created) != 1 or not created[0].get('no_agent') or not created[0].get('enabled')
                or created[0].get('script') != target.name
                or created[0].get('deliver') != 'telegram:' + args.telegram_owner
                or created[0].get('schedule', {}).get('minutes') != 10080):
            raise RuntimeError('Agendamento sem confirmação; consulte o cron antes de anunciar ativação.')
        print('Consulta semanal agendada, sem LLM. Entrega real ainda depende do scheduler/Telegram.')
        print('ID:', created[0]['id'])
        print('Para desativar: hermes cron pause ' + created[0]['id'])


if __name__ == '__main__':
    main()
