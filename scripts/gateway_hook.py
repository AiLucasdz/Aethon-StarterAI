#!/usr/bin/env python3
"""Interface de onboarding chamada pelo agente conforme a instrução no SOUL.

Não é callback nativo nem bloqueia pedidos fora do onboarding.
Saídas: ONBOARDING_ATIVO <chave> ou ONBOARDING_CONCLUIDO.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
BASE_DIR = Path(__file__).resolve().parent.parent
STATE = HERMES_HOME / "state" / "onboarding.json"


def main() -> int:
    # Sem estado de onboarding = dono antigo, fluxo normal
    if not STATE.exists():
        print("ONBOARDING_CONCLUIDO")
        return 0

    # Normaliza a mesma saída ao iniciar, responder, importar ou pular.
    args = sys.argv[1:] or ['--iniciar']
    r = subprocess.run(
        [sys.executable, str(BASE_DIR / 'scripts/onboarding.py'), *args],
        capture_output=True, text=True)
    if r.returncode:
        print("ERRO: onboarding indisponível", file=sys.stderr)
        return r.returncode
    out = r.stdout.strip()
    if out.startswith("ONBOARDING_CONCLUIDO"):
        print(out)
        return 0
    # primeira linha: PERGUNTA:chave; resto: texto da pergunta
    linhas = out.split("\n", 1)
    chave = linhas[0].replace("PERGUNTA:", "")
    pergunta = linhas[1] if len(linhas) > 1 else ""
    print(f"ONBOARDING_ATIVO {chave}")
    print(pergunta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
