#!/usr/bin/env python3
"""Escolhas privadas e extensíveis. Não conecta contas nem instala cron jobs."""
import argparse
import json
import re
from private_state import home, locked, read, write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('acao', choices=['listar', 'solicitar', 'desativar'])
    parser.add_argument('tipo', nargs='?', choices=['conexao', 'rotina'])
    parser.add_argument('id', nargs='?')
    args = parser.parse_args()
    if args.acao != 'listar' and (not args.tipo or not args.id or
            not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', args.id)):
        parser.error('Informe tipo e identificador (letras minúsculas, números, _ ou -).')
    with locked():
        path = home() / 'state' / 'modulos.json'
        state = read(path, {'schema': 1, 'conexoes': {}, 'rotinas': {}})
        if state.get('schema') != 1:
            raise ValueError('Versão de estado não suportada; atualize a base.')
        if args.acao != 'listar':
            group = 'conexoes' if args.tipo == 'conexao' else 'rotinas'
            state[group][args.id] = {
                'desejado': 'solicitado' if args.acao == 'solicitar' else 'desativado',
            }
            write(path, state)
        print(json.dumps(state, ensure_ascii=False, indent=2))
        if args.acao != 'listar':
            print('Escolha registrada. Nenhuma conta ou automação foi alterada por este comando.')
            print('O agente deve executar e verificar a configuração ou interrupção no serviço correspondente.')


if __name__ == '__main__':
    main()
