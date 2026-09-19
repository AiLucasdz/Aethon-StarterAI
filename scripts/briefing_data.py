#!/usr/bin/env python3
"""Dados do briefing calculados no fuso do dono: data, dia da semana, hora.

Uso: briefing_data.py [IANA_TZ]
Env: VAULT_PATH
"""
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

def main() -> int:
    tz = ZoneInfo(sys.argv[1] if len(sys.argv) > 1 else "America/Sao_Paulo")
    agora = datetime.now(tz)
    dias = ["segunda-feira","terça-feira","quarta-feira","quinta-feira",
            "sexta-feira","sábado","domingo"]
    print(f"data: {agora.strftime('%d/%m/%Y')}")
    print(f"dia_da_semana: {dias[agora.weekday()]}")
    print(f"hora: {agora.strftime('%H:%M')}")
    print(f"fuso: {str(tz)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
