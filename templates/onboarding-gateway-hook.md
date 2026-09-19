# Referência de onboarding

O instalador `scripts/iniciar.py` inclui a instrução de onboarding pendente no
**SOUL privado**. Não cole um segundo bloco no AGENTS.md: o fluxo executável e
os caminhos do perfil são gerados pelo instalador.

O agente chama `scripts/gateway_hook.py`, pergunta um item por vez e passa a
resposta com argumentos separados. Ao concluir, `onboarding.py` remove o bloco
pendente do SOUL e projeta a identidade. Não há callback de gateway registrado
por esse script. Pedidos fora do onboarding devem ser atendidos normalmente,
com retomada posterior das perguntas.

Siga [o fluxo completo](../docs/instalar-pelo-telegram.md), incluindo ativação e
validação da memória. Concluir perguntas não comprova instalação concluída.
