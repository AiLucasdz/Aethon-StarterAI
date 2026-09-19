#!/usr/bin/env python3
"""Registra captura no diario diario do dono (Markdown), idempotente.

Uso: diario_registrar.py --tipo captura --origem ORIGEM --texto TEXTO
                      [--data YYYY-MM-DD] [--message-id ID]
Env: VAULT_PATH (default ~/vault)
Message-id repetido nao duplica.
"""
import argparse
import os
import sys
from datetime import date
from pathlib import Path

VAULT = Path(os.environ.get("VAULT_PATH", Path.home() / "vault"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tipo", default="captura",
                   choices=["captura", "checkin", "emocional", "fechamento", "pessoal", "profissional"])
    p.add_argument("--data", default=None)
    p.add_argument("--origem", required=True)
    p.add_argument("--texto", required=True)
    p.add_argument("--message-id", default=None)
    args = p.parse_args()

    dia = args.data or date.today().isoformat()
    VAULT.mkdir(parents=True, exist_ok=True)
    arq = VAULT / "07_DIARIO" / f"{dia}.md"
    arq.parent.mkdir(parents=True, exist_ok=True)

    if args.message_id and arq.exists() and args.message_id in arq.read_text():
        print(f"ja registrado: {args.message_id}")
        return 0

    bloco = f"\n## {args.tipo} — origem: {args.origem}\n\n{args.texto}\n"
    if args.message_id:
        bloco += f"\n<!-- id: {args.message_id} -->\n"
    with arq.open("a") as f:
        f.write(bloco)
    print(arq)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
