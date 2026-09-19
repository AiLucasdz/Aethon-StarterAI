#!/usr/bin/env python3
"""Captura bruta do dono no vault, com message-id estavel (idempotente).

Uso: raw_capture.py --texto "texto cru" --origem telegram:chat --message-id p/c/m
Env: VAULT_PATH
"""
import argparse
import os
import sys
from datetime import date
from pathlib import Path

VAULT = Path(os.environ.get("VAULT_PATH", Path.home() / "vault"))
INBOX = VAULT / "00_INBOX" / "para-processar.md"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--texto", required=True)
    p.add_argument("--origem", required=True)
    p.add_argument("--message-id", default=None)
    args = p.parse_args()

    if args.message_id and INBOX.exists() and args.message_id in INBOX.read_text():
        print(f"ja capturado: {args.message_id}")
        return 0

    INBOX.parent.mkdir(parents=True, exist_ok=True)
    bloco = f"\n## {date.today().isoformat()} — origem: {args.origem}\n\n{args.texto}\n"
    if args.message_id:
        bloco += f"\n<!-- id: {args.message_id} -->\n"
    with INBOX.open("a") as f:
        f.write(bloco)
    print(INBOX)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
