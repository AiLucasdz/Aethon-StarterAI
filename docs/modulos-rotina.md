# Scripts entregues

- iniciar.sh/iniciar.py: templates privados e instrução de onboarding no SOUL.
- onboarding.py/gateway_hook.py: perguntas, estado e perfil. O hook é chamado
  pelo modelo; não é callback registrado automaticamente no gateway.
- diario_registrar.py/raw_capture.py: captura quando invocados; nenhuma rotina
  automática instalada. ID de mensagem com hash exato, lock e escrita atômica.
- briefing_data.py: data no fuso explícito ou escolhido no onboarding.
- soul_sync.py: projeção manual; recusa sobrescrever conteúdo diferente.
- configurar_hermes.sh/configurar_bot.sh: usam o Hermes nativo já instalado.
- update.sh: atualização Git fast-forward; não é migrador do runtime.
- testar-instalacao-limpa.sh: testes locais isolados, sem API ou Telegram.

Demais integrações estão no catálogo como pendentes. Nenhum script de diário
faz push automático. A revisão de privacidade é separada da atualização.
