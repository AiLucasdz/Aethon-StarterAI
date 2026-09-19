#!/usr/bin/env bash
# Tokens e pareamento são responsabilidade do configurador nativo Hermes.
set -euo pipefail
command -v hermes >/dev/null || { echo 'Hermes não encontrado.' >&2; exit 1; }
hermes gateway setup
if [[ -n "${1:-}" ]]; then
  printf 'Nome escolhido: %s\nNo BotFather: /setname e selecione seu bot.\n' "$1"
fi
