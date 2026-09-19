#!/usr/bin/env bash
# Atualiza a camada BASE do template preservando personalização e dados.
# Uso: ./scripts/update.sh   (rodar a partir da raiz do seu fork)
set -euo pipefail

echo "== Backup obrigatório =="
TS=$(date +%F-%H%M)
tar czf ~/backup-hermes-$TS.tar.gz ~/.hermes --exclude='.hermes/hermes-agent' 2>/dev/null \
  || echo "(sem ~/.hermes ainda? backup pulado — primeira instalação)"
echo "backup: ~/backup-hermes-$TS.tar.gz"

echo "== Atualizando base =="
# O git pull só trouxa mudanças da camada base. Preservados por design:
#   - soul/config/memórias vivem FORA do checkout (em ~/.hermes e dados do dono)
#   - nada neste repo aponta para dados reais de usuário
if [ -n "$(git status --porcelain)" ]; then
  echo "AVISO: há mudanças locais na camada base (você modificou o template)."
  echo "O migrador vai parar para você decidir cada conflito."
  git stash list >/dev/null
  git diff --stat
  exit 1
fi

echo "== Verificação de privacidade =="
# Procura padrões de dados reais que não deveriam estar aqui
BANNED="${BANNED_NAMES:-}"  # nomes pessoais separados por | ; defina no seu fork
if [ -n "$BANNED" ]; then
  if git grep -nIiE "($BANNED)" -- . 2>/dev/null | grep -v 'docs/privacidade.md' | head -5; then
    echo "FALHA: possíveis dados pessoais no repositório. Corrija antes de publicar."
    exit 1
  fi
  echo "verificação de privacidade OK (BANNED_NAMES)"
else
  echo "BANNED_NAMES não definido — verificação de privacidade pulada"
fi

echo "OK. Base atualizada; personalização e dados preservados."
