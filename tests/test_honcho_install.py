"""Fluxo do instalador, sem credenciais, conta ou chamada Honcho real."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
with patch.object(sys, 'path', [str(SCRIPTS), *sys.path]):
    spec = importlib.util.spec_from_file_location('install_memory', SCRIPTS / 'ativar-memoria.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


def result(value='null', code=0):
    return SimpleNamespace(returncode=code, stdout=value, stderr='')


class HonchoInstall(unittest.TestCase):
    def call(self, choice='solicitado'):
        return module.configurar_honcho('/fixture/hermes', Path('/fixture/runtime'), {}, choice)

    def test_refusal_and_unanswered_do_not_call_runtime(self):
        with patch.object(module.subprocess, 'run') as run:
            self.assertEqual(self.call('(pulado)')['estado'], 'recusado')
            self.assertEqual(self.call(None)['estado'], 'aguardando_escolha')
            run.assert_not_called()

    def test_existing_honcho_and_other_provider_are_preserved(self):
        for provider, expected in [('"honcho"', 'existente_validacao_pendente'),
                                   ('"outro"', 'conflito_provider')]:
            with patch.object(module.subprocess, 'run', return_value=result(provider)) as run:
                self.assertEqual(self.call()['estado'], expected)
                self.assertEqual(run.call_count, 1)

    def test_no_terminal_returns_safe_resume_without_starting_wizard(self):
        with patch.object(module.subprocess, 'run', return_value=result()) as run, \
             patch.object(module.sys.stdin, 'isatty', return_value=False):
            stage = self.call()
            self.assertEqual(stage['estado'], 'autenticacao_pendente')
            self.assertIn('memory setup honcho', stage['comando_terminal'])
            self.assertIn('HERMES_HOME=/fixture/runtime', stage['comando_terminal'])
            self.assertEqual(run.call_count, 1)

    def test_terminal_executes_native_wizard_but_does_not_claim_validation(self):
        for final, expected in [('"honcho"', 'configurado_validacao_pendente'),
                                ('null', 'setup_incompleto')]:
            with patch.object(module.subprocess, 'run', side_effect=[result(), result(), result(final)]) as run, \
                 patch.object(module.sys.stdin, 'isatty', return_value=True), \
                 patch.object(module.sys.stdout, 'isatty', return_value=True):
                self.assertEqual(self.call()['estado'], expected)
                self.assertEqual(run.call_args_list[1].args[0],
                                 ['/fixture/hermes', 'memory', 'setup', 'honcho'])
