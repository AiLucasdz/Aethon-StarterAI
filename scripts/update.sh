#!/usr/bin/env bash
# Atualiza somente o checkout, por fast-forward; não migra dados privados.
set -euo pipefail
cd "$(dirname "$0")/.."
REMOTE="${1:-upstream}"
BRANCH="${2:-main}"
git rev-parse --verify HEAD >/dev/null
if [[ -n "$(git status --porcelain)" ]]; then
  echo 'Checkout com alterações locais: resolva antes de atualizar.' >&2
  exit 1
fi
git remote get-url "$REMOTE" >/dev/null
OLD=$(git rev-parse HEAD)
git fetch "$REMOTE" "$BRANCH"
NEW=$(git rev-parse FETCH_HEAD)
if ! git merge-base --is-ancestor "$OLD" "$NEW"; then
  echo 'Fork divergente: revisão/merge manual necessário. Nenhum arquivo alterado.' >&2
  exit 1
fi
if [[ "$OLD" == "$NEW" ]]; then echo 'Base já atualizada.'; exit 0; fi
umask 077
BACKUP_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/aethon/base-backups"
mkdir -p "$BACKUP_DIR"
BACKUP=$(mktemp "$BACKUP_DIR/base-XXXXXX.bundle")
git bundle create "$BACKUP" --all
git bundle verify "$BACKUP" >/dev/null
git merge --ff-only "$NEW"
printf 'Base atualizada. Revisão anterior: %s\nBackup do Git: %s\n' "$OLD" "$BACKUP"
echo 'Dados privados não foram migrados nem copiados; este backup é apenas do código.'
