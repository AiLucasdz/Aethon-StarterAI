"""Consulta read-only e instalação idempotente, sem Telegram ou cron de produção."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'scripts'))


def module(name):
    spec = importlib.util.spec_from_file_location(name, BASE / 'scripts' / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


CHECK = module('verificar-atualizacoes')
INSTALL = module('ativar-atualizacoes')


class Updates(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='aethon-weekly-test-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def git(self, repo, *args):
        return subprocess.run(['git', '-C', str(repo), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def test_check_preserves_checkout_and_is_silent_when_current(self):
        origin = self.root / 'origin'; origin.mkdir()
        self.git(origin, 'init', '-b', 'main')
        self.git(origin, 'config', 'user.name', 'Fixture')
        self.git(origin, 'config', 'user.email', 'fixture@example.invalid')
        (origin / 'source').write_text('one')
        self.git(origin, 'add', '.'); self.git(origin, 'commit', '-m', 'one')
        local = self.root / 'local'
        self.git(self.root, 'clone', str(origin), str(local))
        self.assertEqual(CHECK.check(local, str(origin)), '')
        before = self.git(local, 'rev-parse', 'HEAD')
        (local / 'private-change').write_text('preserve')
        (origin / 'source').write_text('two')
        self.git(origin, 'commit', '-am', 'two')
        self.assertIn('atualização pendente', CHECK.check(local, str(origin)))
        self.assertEqual(self.git(local, 'rev-parse', 'HEAD'), before)
        self.assertEqual((local / 'source').read_text(), 'one')
        self.assertEqual((local / 'private-change').read_text(), 'preserve')
        self.git(local, 'merge', '--ff-only', 'FETCH_HEAD')
        self.assertEqual(CHECK.check(local, str(origin)), '')

    def test_failure_does_not_claim_current_or_leak_remote(self):
        with patch.object(CHECK.subprocess, 'run', return_value=subprocess.CompletedProcess([], 1, '', 'secret')):
            with self.assertRaisesRegex(RuntimeError, 'Consulta do template falhou'):
                CHECK.check(self.root, 'https://secret@example.invalid/repo')

    def test_install_is_no_agent_idempotent_and_preserves_pause(self):
        root = self.root / 'runtime'; root.mkdir()
        created = []

        def command(argv, **kwargs):
            args = argv[1:]
            out = ''
            if args == ['config', 'path']:
                out = str(root / 'config.yaml')
            elif args == ['cron', 'create', '--help']:
                out = '--no-agent'
            elif args[:2] == ['cron', 'create']:
                created.append(args)
                self.assertIn('--no-agent', args)
                self.assertEqual(args[args.index('--script') + 1], 'aethon-update-check.py')
                self.assertIn('every 7d', args)
                self.assertIn('telegram:123456789', args)
                (root / 'cron').mkdir()
                (root / 'cron/jobs.json').write_text(json.dumps({'jobs': [dict(
                    id='fixture', name=INSTALL.NAME, enabled=True, no_agent=True,
                    script='aethon-update-check.py', deliver='telegram:123456789',
                    schedule={'kind': 'interval', 'minutes': 10080})]}))
            else:
                self.fail(str(args))
            return subprocess.CompletedProcess(argv, 0, out, '')

        with patch.dict(os.environ, {'HERMES_HOME': str(root)}), \
             patch.object(sys, 'argv', ['install', '--telegram-owner', '123456789']), \
             patch.object(INSTALL.shutil, 'which', return_value='/fake/hermes'), \
             patch.object(INSTALL.subprocess, 'run', side_effect=command):
            INSTALL.main()
            jobfile = root / 'cron/jobs.json'
            data = json.loads(jobfile.read_text()); data['jobs'][0]['enabled'] = False
            jobfile.write_text(json.dumps(data))
            INSTALL.main()
            self.assertEqual(len(created), 1)
            self.assertFalse(json.loads(jobfile.read_text())['jobs'][0]['enabled'])

    def test_group_destination_is_rejected_before_runtime_calls(self):
        with patch.object(sys, 'argv', ['install', '--telegram-owner=-100123']), \
             patch.object(INSTALL.subprocess, 'run') as run:
            with self.assertRaises(SystemExit):
                INSTALL.main()
            run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
