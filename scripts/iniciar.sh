#!/usr/bin/env bash
# Inicializa a instalacao do dono a partir do template Aethon-StarterAI.
# Idempotente: pode rodar varias vezes sem duplicar nada.
# Uso: ./scripts/iniciar.sh
set -euo pipefail

cd "$(dirname "$0")/.."
BASE_DIR="$(pwd)"

echo "════════════════════════════════════════════"
echo "  Aethon-StarterAI — inicializacao da instalacao"
echo "════════════════════════════════════════════"

# ── 1. Caminhos privados ──────────────────────────────
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
VAULT_PATH="${VAULT_PATH:-$HOME/vault}"
echo "runtime:   $HERMES_HOME"
echo "vault:     $VAULT_PATH"

# ── 2. Vault: copia esqueleto se nao existir ──────────
if [ -d "$VAULT_PATH" ] && [ -f "$VAULT_PATH/AGENTS.md" ]; then
  echo "✓ vault ja existe — preservado"
else
  mkdir -p "$VAULT_PATH"
  cp -r "$BASE_DIR/templates/vault/." "$VAULT_PATH/"
  echo "✓ vault criado a partir do template"
fi

# ── 3. Soul: cria a partir do template se nao existir ─
SOUL="$HERMES_HOME/SOUL.md"
if [ -f "$SOUL" ]; then
  echo "✓ soul ja existe — preservado (nunca sobrescrevemos)"
else
  mkdir -p "$HERMES_HOME"
  cp "$BASE_DIR/templates/soul-template.md" "$SOUL"
  echo "✓ soul esqueleto criado em $SOUL"
  echo "  → preencha via onboarding no Telegram (docs/onboarding.md)"
fi

# ── 4. Executaveis ────────────────────────────────────
chmod +x "$BASE_DIR"/scripts/*.py 2>/dev/null || true
echo "✓ scripts executaveis"

# ── 5. Sanity check ───────────────────────────────────
python3 "$BASE_DIR/scripts/briefing_data.py" > /dev/null && echo "✓ briefing_data OK"
echo "✓ estrutura pronta"

# ativa o onboarding: cria o estado para o gateway hook saber que esta pendente
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/onboarding.py" --iniciar > /dev/null 2>&1 || true
echo "✓ onboarding pendente — sera executado na primeira mensagem do dono no Telegram"
echo ""
echo "Próximos passos:"
echo "  1. Conecte o bot ao Telegram (video de instalacao)"
echo "  2. O agente faz o onboarding sozinho na primeira mensagem (docs/onboarding.md)"
echo "  3. Ativar conexoes: docs/catalogo-modulos.md"
echo "  4. Atualizacoes futuras: scripts/update.sh"
