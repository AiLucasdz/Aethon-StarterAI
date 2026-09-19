import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('memory_plugin', BASE / 'plugins/aethon-memory/__init__.py')
plugin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(plugin)


class Memory(unittest.TestCase):
    def test_current_sources_without_stale_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            source = vault / 'AGENTS.md'
            source.write_text('## Jardim plantas\nUsar jardim antigo.\n')
            self.assertIn('antigo', plugin.local_passages(vault, 'Jardim plantas')[0]['text'])
            source.write_text('## Jardim plantas antigo\nEstado: superado.\nRegra antiga.\n'
                              '## Jardim plantas atual\nRegra confirmada.\n')
            rows = plugin.local_passages(vault, 'Jardim plantas')
            self.assertEqual(len(rows), 1)
            self.assertIn('confirmada', rows[0]['text'])

    def test_bound_and_remote_contract(self):
        data = {'facts': [{'fact': 'Jardim antigo', 'source': 'old', 'expired_at': '2026-01-01'},
                          {'fact': 'Assunto sem relação', 'source': 'other'},
                          {'fact': 'Jardim confirmado', 'source': 'nota', 'fact_id': '1'}],
                'results': [{'title': 'Só metadados'}, {'chunk': 'Trecho completo', 'slug': 'jardim'}]}
        rows = plugin.remote_passages(plugin.unpack({'ok': True, 'result': json.dumps(data)}), 'Jardim')
        self.assertEqual(len(rows), 2)
        local = [{'source': 'nota', 'text': 'x' * 1700}] * 2
        remote = [{'source': 'indice', 'text': 'y' * 1200}] * 3
        context = plugin.build_context(Path('/fixture'), local, remote, 'ok')
        self.assertLessEqual(len(context), 6000)
        parsed = json.loads(context.split('<aethon_memory_data>\n')[1].split('\n</aethon_memory_data>')[0])
        self.assertEqual(parsed['fontes_locais_atuais'], local)
        self.assertEqual(len(remote), 3)

    def test_privacy_and_degraded_recall(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / 'AGENTS.md').write_text('## Jardim plantas\nRegra atual.\n')
            with sqlite3.connect(home / 'state.db') as db:
                db.execute('CREATE TABLE sessions(id,chat_type,user_id,chat_id)')
                db.executemany('INSERT INTO sessions VALUES(?,?,?,?)',
                               [('dm', 'dm', '123', '123'), ('group', 'group', '123', '-1')])
            class Context:
                calls = 0
                def get_config(self, key, default=None):
                    return {'home': str(home), 'vault': str(home), 'owner_id': '123',
                            'gbrain_enabled': True}.get(key, default)
                def register_hook(self, name, callback):
                    self.callback = callback
                def call_mcp(self, *args, **kwargs):
                    self.calls += 1
                    raise TimeoutError('fixture')
            ctx = Context()
            plugin.register(ctx)
            with patch.dict('sys.modules', {'hermes_constants': SimpleNamespace(get_hermes_home=lambda: home)}):
                for options in [{'platform': 'telegram', 'sender_id': '123', 'session_id': 'group'},
                                {'platform': 'telegram', 'sender_id': '999', 'session_id': 'dm'},
                                {'platform': 'cron'}, {'platform': 'cli', 'parent_session_id': 'parent'}]:
                    self.assertIsNone(ctx.callback(user_message='Jardim plantas', **options))
                self.assertEqual(ctx.calls, 0)
                result = ctx.callback(user_message='Jardim plantas', platform='telegram', sender_id='123', session_id='dm')
                self.assertIn('Regra atual.', result['context'])
                self.assertIn('TimeoutError', result['context'])
                self.assertIn('Informe brevemente ao usuário', result['context'])
                self.assertIn('Não confunda falha com ausência', result['context'])
                self.assertEqual(ctx.calls, 1)
                with patch.object(plugin, 'direct_session', side_effect=AssertionError('I/O extra')):
                    self.assertIsNone(ctx.callback(user_message='ok', platform='telegram'))


if __name__ == '__main__':
    unittest.main()
