"""Append com deduplicação exata por hash de ID e bloqueio entre processos."""
import fcntl
import hashlib
import os
import tempfile
from private_state import safe


def append_once(path, text, message_id):
    path = safe(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(path.suffix + '.lock')
    if lock.is_symlink():
        raise ValueError('Lock é symlink')
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as guard:
        fcntl.flock(guard, fcntl.LOCK_EX)
        old = path.read_text() if path.exists() else ''
        marker = ('<!-- capture-id: ' + hashlib.sha256(message_id.encode()).hexdigest() + ' -->') if message_id else None
        if marker and marker in old.splitlines():
            return False
        out = old + text + ('\n' + marker + '\n' if marker else '')
        tmpfd, tmp = tempfile.mkstemp(dir=path.parent)
        try:
            with os.fdopen(tmpfd, 'w') as stream:
                stream.write(out)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    return True
