#!/usr/bin/env bash
# Testes locais isolados: não representam instalação real de Hermes/Telegram.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -v
