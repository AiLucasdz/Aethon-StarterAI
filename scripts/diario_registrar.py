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

    dia = date.fromisoformat(args.data).isoformat() if args.data else date.today().isoformat()
    VAULT.mkdir(parents=True, exist_ok=True)
    arq = VAULT / "07_DIARIO" / f"{dia}.md"
    arq.parent.mkdir(parents=True, exist_ok=True)


    bloco = f"\n## {args.tipo} — origem: {args.origem}\n\n{args.texto}\n"

    from capture_store import append_once
    append_once(arq, bloco, args.message_id)
    print(arq)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
