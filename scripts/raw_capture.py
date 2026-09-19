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


    bloco = f"\n## {date.today().isoformat()} — origem: {args.origem}\n\n{args.texto}\n"

    from capture_store import append_once
    append_once(INBOX, bloco, args.message_id)
    print(INBOX)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
