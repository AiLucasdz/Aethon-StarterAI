# Próxima versão — revisão após v0.2.1

- Entrada pelo link do repositório no Telegram já conectado; o agente instala,
  preserva a configuração existente e inicia as perguntas, uma de cada vez.
- Onboarding retomável, sem pedir tokens, bloquear ajuda ou anunciar backup
  inexistente. Nome do agente vem primeiro; todas as etapas podem ser puladas.
- Conexões e automações opcionais, independentes e extensíveis. Registro privado
  de escolhas não representa autenticação ou agendamento real.
- Base operacional atualizável no SOUL, migração versionada com backup local,
  reversão e detecção de conflitos; texto personalizado e módulos preservados.
- Perfil de desempenho opt-in com max_turns=25, compactação de 300 mil tokens
  e tail lean. Instalação e migração não aplicam esse perfil automaticamente.
- Atualização Git por fast-forward com bundle verificado; forks divergentes
  exigem revisão. O update.sh não migra runtime nem atualiza o Hermes.
- Capturas com deduplicação por ID exato, escrita atômica e validação de datas.
- Dados privados fora do checkout; rejeição de symlinks nos caminhos tratados.

Validação local: nove testes isolados passaram, incluindo atualização/reversão,
interrupção e preservação de personalizações. Teste offline com Hermes instalado
passou: instalação fictícia, leitura da configuração, backup/import do runtime e
migração após restauração. Não comprova entrega Telegram, comportamento do modelo,
OAuth, backup do vault externo ou desempenho em VPS KVM 1.

Pendentes: vídeo, bot de teste real, adaptadores opcionais autenticados, backup
integral/externo, revisão completa dos metadados do histórico e próxima release.
