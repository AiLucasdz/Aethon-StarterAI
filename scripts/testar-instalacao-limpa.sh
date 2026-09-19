#!/usr/bin/env bash
# Simula a instalacao de OUTRA PESSOA do zero, isolada de qualquer instalacao pessoal.
# Nao usa Docker (nao ha na VPS): cria um sandbox com HOME falso e roda o ciclo
# completo — iniciar.sh -> configurar_hermes.sh (entradas simuladas) ->
# gateway hook (primeira mensagem -> respostas -> conclusao).
# Uso: ./scripts/testar-instalacao-limpa.sh
set -uo pipefail

BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SANDBOX=$(mktemp -d)
FAKE_HOME="$SANDBOX/home"
mkdir -p "$FAKE_HOME"

echo "════ Simulação: outra pessoa instalando do zero ════"
echo "sandbox: $SANDBOX"
FAIL=0
check() { # check <descricao> <esperado> <obtido>
  if [[ "$2" == *"$3"* ]]; then echo "✓ $1"; else echo "✗ $1"; echo "  esperado conter: $3"; echo "  obtido: $2"; FAIL=1; fi
}

export HERMES_HOME="$FAKE_HOME/.hermes"
export VAULT_PATH="$FAKE_HOME/vault"
export HOME="$FAKE_HOME"

# ── 1. iniciar.sh cria vault + soul e ativa onboarding ──
OUT=$(bash "$BASE_DIR/scripts/iniciar.sh" 2>&1)
check "iniciar.sh cria vault" "$OUT" "vault criado"
check "iniciar.sh cria soul" "$OUT" "soul esqueleto criado"
check "iniciar.sh ativa onboarding" "$OUT" "onboarding pendente"
[ -f "$VAULT_PATH/07_DIARIO/README.md" ] && echo "✓ pasta 07_DIARIO existe" || { echo "✗ 07_DIARIO"; FAIL=1; }

# ── 2. configurar_hermes.sh aplica modelo/yolo/stt (entradas simuladas) ──
printf 'sk-or-simulada\nz-ai/glm-5.3-flash\n' | bash "$BASE_DIR/scripts/configurar_hermes.sh" > /dev/null 2>&1
check "modelo configurado" "$(cat $HERMES_HOME/config.yaml)" "provider: openrouter"
check "yolo mode" "$(cat $HERMES_HOME/config.yaml)" "mode: 'off'"
check "stt pt" "$(cat $HERMES_HOME/config.yaml)" "stt:"

# ── 3. primeira mensagem do dono: hook ativa onboarding pelo NOME ──
OUT=$(python3 "$BASE_DIR/scripts/gateway_hook.py")
check "hook pergunta o NOME primeiro" "$OUT" "como você quer me chamar"

# ── 4. respostas: nome e fluxo completo (GitHub pulado) ──
python3 "$BASE_DIR/scripts/gateway_hook.py" --responder nome "Kaique" > /dev/null
for r in "dono_nome|Ana" "dono_faz|Advogada" "dono_desejos|prazos" "dono_limites|" "estilo|curtas" "fuso|America/Sao_Paulo" "bot_telegram|pronto" "github_token|pular"; do
  k="${r%%|*}"; v="${r#*|}"
  OUT=$(python3 "$BASE_DIR/scripts/gateway_hook.py" --responder "$k" "$v" 2>&1)
done
check "onboarding concluido" "$OUT" "ONBOARDING_CONCLUIDO"
check "usa o nome escolhido" "$OUT" "Kaique"

# ── 5. soul e perfil preenchidos, sem placeholders ══
SOUL="$HERMES_HOME/SOUL.md"
if grep -q '{{' "$SOUL"; then echo "✗ soul com placeholders restantes"; FAIL=1; else echo "✓ soul sem placeholders"; fi
check "soul com nome escolhido" "$(grep 'Meu nome' $SOUL)" "Kaique"
check "perfil do dono" "$(grep 'Nome:' $VAULT_PATH/01_IDENTIDADE/perfil.md)" "Ana"

# ── 6. token do dono nunca em arquivo versionado ──
if grep -rq 'ghp_\|sk-or-simulada' "$BASE_DIR" --exclude='testar-instalacao-limpa.sh' 2>/dev/null; then echo "✗ segredo vazou para o template"; FAIL=1; else echo "✓ nenhum segredo no template"; fi

# ── 7. limpeza ──
rm -rf "$SANDBOX"

echo ""
if [ $FAIL -eq 0 ]; then
  echo "════ RESULTADO: TODOS OS TESTES PASSARAM ════"
else
  echo "════ RESULTADO: FALHAS ACIMA ════"
fi
exit $FAIL
