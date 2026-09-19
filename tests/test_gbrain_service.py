"""Supervisão e retomada sem abrir PGLite em paralelo; sem serviço real nesta suíte."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import gbrain_service as g


class SharedMemory(unittest.TestCase):
    def test_unavailable_supervisor_does_not_touch_database(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(g, 'systemctl', side_effect=RuntimeError('no supervisor')), \
             patch.object(g.subprocess, 'run') as run:
            root = Path(tmp)
            with self.assertRaises(RuntimeError):
                g.install(root, root, '/fixture/gbrain', root / 'brain', {})
            run.assert_not_called()
            self.assertEqual(list(root.iterdir()), [])

    def test_http_loopback_private_token_and_resume_without_database_reopen(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(g, 'systemctl') as ctl, patch.object(g, 'wait_ready'), \
             patch.object(g.shutil, 'which', return_value='/fixture/bun'), \
             patch.dict(os.environ, {'XDG_CONFIG_HOME': tmp + '/config'}):
            root = Path(tmp) / 'runtime'; root.mkdir()
            token = 'gbrain_' + 'a' * 64
            with patch.object(g.subprocess, 'run', return_value=SimpleNamespace(
                    returncode=0, stdout=token)) as run:
                server = g.install(root, root, '/fixture/gbrain', root / 'brain', {})
                self.assertTrue(server['url'].startswith('http://127.0.0.1:'))
                self.assertNotIn('command', server)
                self.assertNotIn(token, json.dumps(server))
                self.assertEqual((root / '.env').stat().st_mode & 0o777, 0o600)
                receipt = json.loads((root / 'state/aethon-memory/gbrain-service.json').read_text())
                unit = Path(receipt['unit_path']).read_text()
                self.assertIn('Restart=always', unit)
                self.assertIn('--bind 127.0.0.1', unit)
                self.assertNotIn(token, unit)
                run.reset_mock()
                self.assertEqual(g.install(root, root, '/fixture/gbrain', root / 'brain', {}), server)
                run.assert_not_called()
                receipt['brain_home'] = '/fixture/other-brain'
                g.write(root / 'state/aethon-memory/gbrain-service.json', receipt)
                with self.assertRaisesRegex(RuntimeError, 'outro perfil'):
                    g.install(root, root, '/fixture/gbrain', root / 'brain', {})
                run.assert_not_called()

    def test_unit_quoting_rejects_injected_directives(self):
        with self.assertRaises(ValueError): g.quote('/tmp/a\nExecStart=evil')
        self.assertEqual(g.quote('/tmp/10%'), '"/tmp/10%%"')
