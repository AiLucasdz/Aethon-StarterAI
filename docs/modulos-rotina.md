# Scripts e pontos de execução

| Componente | O que executa |
|---|---|
| `iniciar.sh` / `iniciar.py` | Cria templates privados ausentes e prepara onboarding no SOUL |
| `onboarding.py` / `gateway_hook.py` | Perguntas, retomada e projeção de identidade; chamados pelo agente, não callback nativo |
| `migrar.py` | Status, atualização do bloco gerenciado e rollback com preservação de personalizações |
| `ativar-memoria.py` | Instala/preserva GBrain, configura plugin e inicia setup Honcho aceito; sem terminal informa pendência |
| `plugins/aethon-memory` | Recuperação antes do turno pelo hook nativo do Hermes; não escreve memórias |
| `modulos.py` | Registro de intenção/estado, sem instalar conectores nem agendar rotinas |
| `raw_capture.py` / `diario_registrar.py` | Captura quando invocados, com ID exato, lock e escrita atômica |
| `briefing_data.py` | Data no fuso explícito ou escolhido no onboarding |
| `soul_sync.py` | Projeção manual; recusa sobrescrever conteúdo diferente |
| `configurar_hermes.sh` / `configurar_bot.sh` | Acionam a configuração nativa do Hermes já instalado |
| `update.sh` | Atualização Git fast-forward, com backup; migração privada é etapa separada |
| `testar-instalacao-limpa.sh` | Testes locais isolados |
| `testar-runtime.py` | Teste isolado com Hermes/GBrain reais, sem Telegram ou conta Honcho |

Nada aqui instala check-in diário ou faz push automático de memórias. Conectores
externos dependem do [fluxo próprio](conectores.md), configuração e validação.
