"""Consumidor Hermes/GBrain real, só no perfil fictício criado por testar-runtime.py."""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import urllib.request
import urllib.error
import time
from types import SimpleNamespace

home = Path(os.environ['HERMES_HOME'])
vault = Path(os.environ['VAULT_PATH'])
assert home.parent.name.startswith('aethon-runtime-test-') and home.name == 'runtime'

from dotenv import load_dotenv
load_dotenv(home / '.env')

from agent.prompt_builder import load_soul_md
from agent.turn_context import _collect_pre_llm_call_context, build_api_messages
from hermes_cli.plugins import discover_plugins, PluginContext
from tools.mcp_tool_discovery import discover_mcp_tools
from tools.mcp_tool_handlers import _make_tool_handler
from tools.mcp_tool_lifecycle import shutdown_mcp_servers

soul = load_soul_md()
assert 'Aurora' in soul and str(vault / 'AGENTS.md') in soul
assert 'Captura e ancoragem' not in soul  # Não depender de documento não consumido.
fact = 'No projeto fictício Jardim, a decisão confirmada é plantar alecrim no sábado.'
source = '08_DECISOES/decisoes.md#jardim'
with (vault / '08_DECISOES/decisoes.md').open('a') as f:
    f.write('\n## Jardim\n- Estado: vigente.\n' + fact + '\n')
with sqlite3.connect(home / 'state.db') as db:
    db.execute('CREATE TABLE IF NOT EXISTS sessions(id TEXT, chat_type TEXT, user_id TEXT, chat_id TEXT)')
    db.execute("INSERT INTO sessions(id,chat_type,user_id,chat_id) VALUES('fixture-dm','dm','123456','123456')")
    db.execute("INSERT INTO sessions(id,chat_type,user_id,chat_id) VALUES('fixture-group','group','123456','-1')")

def call(tool, arguments):
    envelope = PluginContext._mcp_envelope(_make_tool_handler('gbrain', tool, 20)(arguments))
    assert envelope.get('ok'), envelope
    result = envelope['result']
    return json.loads(result) if isinstance(result, str) else result

try:
    tools = discover_mcp_tools(allowed_mcp_names=['gbrain'])
    assert len(tools) >= 2
    args = {'fact': fact, 'entity': 'jardim', 'provenance': source, 'kind': 'fact', 'visibility': 'world'}
    first = call('remember', args)
    recall = call('recall', {'entity': 'jardim', 'budget_tokens': 1800})
    matches = [row for row in recall.get('facts', []) if row.get('fact') == fact
               and (row.get('source') or row.get('provenance')) == source]
    assert len(matches) == 1, recall
    # Repetição de captura: reaproveita o fato recuperado, sem segunda escrita.
    assert str(matches[0].get('fact_id', matches[0].get('id'))) == first['id']
    # A second Hermes process must read the same fact while this connection is open.
    code = '''
from tools.mcp_tool_discovery import discover_mcp_tools
from tools.mcp_tool_handlers import _make_tool_handler
from tools.mcp_tool_lifecycle import shutdown_mcp_servers
try:
 assert len(discover_mcp_tools(allowed_mcp_names=['gbrain'])) == 7
 result = _make_tool_handler('gbrain', 'recall', 20)({'entity':'jardim'})
 assert 'alecrim' in str(result)
finally: shutdown_mcp_servers(names={'gbrain'})
'''
    subprocess.run([sys.executable, '-c', code], check=True, capture_output=True, timeout=35)
    service = json.loads((home / 'state/aethon-memory/gbrain-service.json').read_text())
    unit, url = service['unit'], service['server']['url']
    def service_value(key):
        return subprocess.check_output(['systemctl', '--user', 'show', unit, '--value', '-p', key], text=True).strip()
    pid = service_value('MainPID')
    subprocess.run(['systemctl', '--user', 'kill', '--kill-whom=main', '--signal=SIGTERM', unit], check=True)
    for _ in range(80):
        time.sleep(.25)
        try:
            if service_value('MainPID') not in ('0', pid):
                urllib.request.urlopen(url.replace('/mcp', '/health'), timeout=1).close()
                break
        except OSError:
            pass
    else:
        raise AssertionError('Isolated GBrain did not automatically recover')
    assert 'alecrim' in str(call('recall', {'entity': 'jardim'}))
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=b'{}', headers={'Content-Type': 'application/json'}))
        raise AssertionError('MCP accepted unauthenticated access')
    except urllib.error.HTTPError as error:
        assert error.code == 401
    discover_plugins()
    agent = SimpleNamespace(session_id='fixture-dm', model='fixture-no-api', platform='telegram',
                            _user_id='123456', _parent_session_id='', _current_turn_timestamp=time.time(),
                            ephemeral_system_prompt='', _copy_reasoning_content_for_api=lambda *a: None,
                            _should_sanitize_tool_calls=lambda: False)
    question = 'Qual foi a decisão do projeto Jardim?'
    messages = [{'role': 'user', 'content': question}]
    started = time.monotonic()
    context = _collect_pre_llm_call_context(agent, effective_task_id='fixture', turn_id='fixture',
                    original_user_message=question, messages=messages, conversation_history=[])
    assert fact in context and source in context and len(context) <= 6000, context
    api_messages, _ = build_api_messages(agent, messages, current_turn_user_idx=0,
                    ext_prefetch_cache='', plugin_user_context=context, moa_config=None, active_system_prompt=soul)
    assert fact in api_messages[-1]['content'] and messages[0]['content'] == question
    agent.session_id = 'fixture-group'
    assert not _collect_pre_llm_call_context(agent, effective_task_id='fixture', turn_id='group',
                    original_user_message=question, messages=messages, conversation_history=[])
    print(json.dumps({'roundtrip': True, 'concurrent_consumers': True, 'automatic_recovery': True, 'unauthenticated_rejected': True, 'read_before_write_reuses_id': True, 'native_wire_context': True,
                      'group_blocked': True, 'context_chars': len(context),
                      'seconds': round(time.monotonic() - started, 3)}))
finally:
    shutdown_mcp_servers(names={'gbrain'})
