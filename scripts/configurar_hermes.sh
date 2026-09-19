#!/usr/bin/env bash
# Configura o Hermes da instalacao do dono: modelo, yolo mode, stt, memoria.
# Idempotente. Roda DEPOIS do video de instalacao (Hermes ja instalado).
# Uso: ./scripts/configurar_hermes.sh
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG="$HERMES_HOME/config.yaml"

echo "════ Configuracao do Hermes ════"

# ── 1. Modelo via OpenRouter (chave do dono, nunca a de outra pessoa) ──
if ! grep -q "provider: openrouter" "$CONFIG" 2>/dev/null; then
  echo "Configure o modelo:"
  read -rp "Chave OpenRouter (sk-or-...): " ORKEY
  read -rp "Modelo (enter = z-ai/glm-5.3-flash): " ORMODEL
  ORMODEL="${ORMODEL:-z-ai/glm-5.3-flash}"
  if [ ! -f "$HERMES_HOME/.env" ]; then touch "$HERMES_HOME/.env"; fi
  grep -q OPENROUTER_API_KEY "$HERMES_HOME/.env" 2>/dev/null || \
    printf 'OPENROUTER_API_KEY=%s\n' "$ORKEY" >> "$HERMES_HOME/.env"
  python3 - "$CONFIG" "$ORMODEL" <<'EOF'
import sys
from pathlib import Path
cfg, model = Path(sys.argv[1]), sys.argv[2]
t = cfg.read_text() if cfg.exists() else ""
if "model:" not in t:
    t += f"\nmodel:\n  default: {model}\n  provider: openrouter\n"
cfg.write_text(t)
EOF
  echo "✓ modelo: $ORMODEL via OpenRouter"
else
  echo "✓ modelo ja configurado"
fi

# ── 2. Yolo mode (approvals off) ──
python3 - "$CONFIG" <<'EOF'
import sys
from pathlib import Path
cfg = Path(sys.argv[1])
t = cfg.read_text() if cfg.exists() else ""
if "approvals:" not in t:
    t += "\napprovals:\n  mode: 'off'\n  mcp_reload_confirm: false\n  destructive_slash_confirm: false\n"
    cfg.write_text(t)
    print("✓ yolo mode: approvals off")
else:
    print("✓ approvals ja configurado")
EOF

# ── 3. STT local em portugues (audio do Telegram) ──
python3 - "$CONFIG" <<'EOF'
import sys
from pathlib import Path
cfg = Path(sys.argv[1])
t = cfg.read_text() if cfg.exists() else ""
if "stt:" not in t:
    t += "\nstt:\n  language: pt\n  local:\n    model: small\n    language: pt\n"
    cfg.write_text(t)
    print("✓ stt local pt (audio do Telegram vira texto)")
else:
    print("✓ stt ja configurado")
EOF

# ── 4. max_turns ──
python3 - "$CONFIG" <<'EOF'
import sys
from pathlib import Path
cfg = Path(sys.argv[1])
t = cfg.read_text() if cfg.exists() else ""
if "max_turns:" not in t:
    t += "\nagent:\n  max_turns: 25\n"
    cfg.write_text(t)
    print("✓ agent.max_turns: 25")
else:
    print("✓ max_turns ja configurado")
EOF

echo ""
echo "Pronto. Reinicie o gateway para aplicar:"
echo "  hermes gateway restart"
