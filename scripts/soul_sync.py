#!/usr/bin/env python3
"""Projeta o soul versionado para o caminho do runtime.

Uso: python3 soul_sync.py <soul-fonte.md> [destino]
Env: HERMES_HOME (default ~/.hermes)
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    src = Path(sys.argv[1]).expanduser()
    if not src.exists():
        print(f"fonte nao encontrada: {src}")
        return 1
    dst = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else HERMES_HOME / "SOUL.md"
    if dst.is_symlink() or any(p.is_symlink() for p in dst.parents):
        print("Destino com symlink; projeção recusada")
        return 1
    dst.parent.mkdir(parents=True, exist_ok=True)
    changed = True
    if dst.exists():
        h_src = hashlib.sha256(src.read_bytes()).hexdigest()
        h_dst = hashlib.sha256(dst.read_bytes()).hexdigest()
        changed = h_src != h_dst
    if changed:
        if dst.exists():
            print("Destino diferente já existe; faça revisão e backup manual. Não sobrescrito.")
            return 1
        fd = os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as f:
            f.write(src.read_bytes())
        print(f"soul sincronizado: {src} -> {dst}")
    else:
        print("soul ja sincronizado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
