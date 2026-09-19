#!/usr/bin/env bash
# Conecta o bot do Telegram e renomeia para o nome escolhido no onboarding.
# Uso: ./scripts/configurar_bot.sh [NOME_DO_AGENTE]
set -euo pipefail

NOME="${1:-}"

if ! grep -q "TELEGRAM_BOT_TOKEN" "$HOME/.hermes/.env" 2>/dev/null; then
  echo "1. Fale com @BotFather no Telegram: /newbot"
  echo "2. Copie o token"
  read -rp "Token do BotFather: " TOK
  printf 'TELEGRAM_BOT_TOKEN=%s\n' "$TOK" >> "$HOME/.hermes/.env"
  echo "✓ token salvo em ~/.hermes/.env (permissao do arquivo preservada)"
fi

if [ -n "$NOME" ]; then
  echo ""
  echo "Para o nome aparecer no Telegram, mude manualmente no @BotFather:"
  echo "  /setname → escolha seu bot → $NOME"
  echo "  /setdescription → descricao curta do agente"
  echo "  /setuserpic → uma foto, se quiser"
fi

echo ""
echo "Reinicie o gateway para conectar:"
echo "  hermes gateway restart"
