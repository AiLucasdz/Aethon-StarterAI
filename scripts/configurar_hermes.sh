#!/usr/bin/env bash
# Usa o configurador nativo, preservando escolhas já feitas.
set -euo pipefail
command -v hermes >/dev/null || { echo 'Hermes não encontrado. Instale pelo guia oficial.' >&2; exit 1; }
hermes config check
printf '%s\n' 'Para escolher GLM ou DeepSeek via OpenRouter, use: hermes model' 'Não cole chaves no Telegram. Use o configurador nativo no terminal.'
if [[ "${1:-}" == '--perfil-leve' ]]; then
  hermes config set agent.max_turns 25
  hermes config set compression.enabled true
  hermes config set compression.threshold_tokens 100000
  hermes config set compression.tail_mode lean
  echo 'Perfil leve aplicado. Não altera modelo, aprovações, STT ou provedores de memória.'
fi

if [[ "${1:-}" == '--yolo' ]]; then
  hermes config set approvals.mode off
  echo 'Aprovações de execução desativadas por escolha explícita. Não concede sudo.'
fi
