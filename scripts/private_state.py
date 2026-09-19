"""Operações compartilhadas para estado privado do template."""
import contextlib
import fcntl
import json
import os
from pathlib import Path
import tempfile

BASE = Path(__file__).resolve().parents[1]


def safe(path):
    path = Path(path).expanduser().absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('Caminho privado contém symlink')
    if path.resolve().is_relative_to(BASE):
        raise ValueError('Estado privado não pode ficar no checkout')
    return path


def home():
    return safe(os.environ.get('HERMES_HOME', Path.home() / '.hermes'))


def read(path, default=None):
    path = safe(path)
    return json.loads(path.read_text()) if path.exists() else default


def atomic(path, data):
    path = safe(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write(path, data):
    atomic(path, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())


@contextlib.contextmanager
def locked():
    state = safe(home() / 'state')
    state.mkdir(parents=True, exist_ok=True, mode=0o700)
    path = safe(state / 'aethon.lock')
    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        yield
