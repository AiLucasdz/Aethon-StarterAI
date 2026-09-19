# Alterações

## Não lançado — aviso semanal sem LLM

- Consulta do repositório oficial a cada sete dias pelo cron nativo; silêncio
  sem novidade e aviso Telegram quando houver atualização pendente.
- Instalação idempotente preserva pausas; aplicação continua dependendo de pedido.
- Verificação não faz merge nem migração e não chama modelo de IA.

## Não lançado — atualização por conversa

- Encerramento do onboarding ensina o pedido de atualização pelo Telegram e a
  possibilidade de consulta semanal, sem anunciar um timer inexistente.
- Base gerenciada aponta para o guia de atualização e distingue consultar de
  aplicar, preservando dados, personalizações e escolhas de runtime.

## Não lançado — preparação antes da apresentação

- Pastas, arquivos privados, GBrain e configuração de áudio preparados antes
  das perguntas de nome e perfil; instrução gerada no SOUL segue a mesma ordem.
- Whisper medium local em CPU/int8 como padrão de instalação, com descarregamento
  após 120 segundos sem uso, teste nativo e tratamento explícito de falta de recursos.
- Escolhas existentes preservadas; nenhuma migração automática de STT ao atualizar.

## Não lançado — avaliação de transcrição local

- Guia de mídia distingue modelo local e identificador de API, exige comparação
  de precisão, latência e memória e não torna modelo maior padrão universal.
- Teste sintético comprova execução, sem prometer precisão com voz natural.

## Não lançado — apresentação livre

- Nome seguido de apresentação por texto, áudio ou documento, organizada pelo
  agente em lote. Perguntar somente lacunas; removidas perguntas repetidas de
  perfil, nome do bot e backup. Compatibilidade com estados antigos preservada.
- Registro privado da apresentação com origem e perfil validado, sem LLM adicional
  no script. Nome já projetado durante a configuração.
- Áudio/documentos dependem de extração real; Honcho local e nuvem distinguem
  custos e dados, sem prometer provisionamento automático de Ollama.

## Não lançado — configuração executada pelo agente

- Responsabilidade explícita por pastas, caminhos, arquivos, comandos e validação.
  Perguntar apenas dados/decisões faltantes; não transferir a execução ao dono.
- Skills após a configuração principal; bloqueio opcional não interrompe
  identidade, onboarding ou memória. Guias de entrada alinhados ao pedido no Telegram.

## Não lançado — apresentação e diagramas

- README orientado a empreendedores, empresários, profissionais e uso pessoal,
  com exemplos concretos; modelos recomendados não restringem a escolha.
- Diagrama de arquitetura público em PNG e HTML, com fonte JSON reproduzível.
- Archify no fluxo de instalação via Hermes, descoberta sob demanda e respeito
  ao scanner; exceções exigem revisão e autorização, sem liberação automática.
- Autoria pública do mantenedor preservada com e-mail GitHub noreply.

## Não lançado — revisão de organização e privacidade

- README reorganizado com fluxo de início, fontes privadas, memória, limites de
  validação, backup e testes. Guias antigos alinhados ao onboarding no SOUL,
  Honcho opcional e GBrain como parte da instalação.
- Escritas privadas recusam checkout público e caminhos com symlinks ancestrais,
  inclusive em capturas e preenchimento do perfil. Ajuda do onboarding sem efeitos.
- Conectores documentados como configuração dependente da instalação; removidos
  exemplos que transportavam código OAuth em argumentos e promessas de rotinas.
- Auditoria de privacidade deve incluir autoria/committer e referências históricas;
  varrer apenas o conteúdo dos arquivos não comprova histórico livre de dados pessoais.

## Não lançado — iniciar e configurar Honcho no mesmo fluxo

- “Iniciar”, “começar”, “configurar” e “instalar” autorizam o mesmo fluxo quando
  associados ao repositório; não exigir palavra específica nem nova confirmação.
- Instalador de memória passa a executar a etapa Honcho escolhida no onboarding:
  wizard nativo em terminal interativo, retomada segura sem terminal, recusa
  respeitada e providers existentes preservados. Estado não confunde configuração
  com recuperação/gravação validadas; nenhuma credencial no comando ou no chat.

## Segundo cérebro como função padrão

- GBrain incluído na instalação: base privada sem chave, busca textual, importação
  inicial e MCP nativo; novas dependências fixadas em GBrain v0.46.12.3,
  integração existente preservada. Honcho oferecido no
  onboarding com recusa permitida. Antigo estado segundo_cerebro compatível.
- Hook de recuperação Hermes com perfil/DM restritos, limite de contexto, sem
  LLM adicional e sem outro processo de banco. Captura semântica com origem,
  decisões e lições específicas, recuperação e aplicação verificáveis.
- SOUL gerenciado recebe caminhos absolutos e escolhas mesmo quando a identidade
  anterior não tem placeholders; personalizações externas preservadas.
- Corrigido bloqueio aninhado no registro de escolhas do onboarding.
- Dezesseis testes isolados e fluxo com Hermes/GBrain reais aprovados: SOUL
  preexistente, recuperação/injeção nativas, bloqueio de grupo, reativação
  idempotente, rollback de config, backup e restauração do runtime. Sem chamadas
  de modelo, Honcho remoto ou instalação completa pelo Telegram nesta validação.
- Fluxo de instalação/atualização documenta ativação e prova no consumidor;
  nenhum dado pessoal nem credencial acompanha a distribuição.

## v0.3.0 — Segundo cérebro (GBrain + Honcho)

- GBrain (MIT, github:garrytan/gbrain) e Honcho como módulos disponíveis;
  guia completo em docs/segundo-cerebro.md. Desligados por padrão.
- Onboarding pergunta "segundo cérebro" (sim/pular); "sim" registra intenção
  de gbrain e honcho no registro de conexões — não instala nada.
- Instrução de sistema ganha Captura e ancoragem (vault antes de indexar,
  --entity, --kind) e Ressurgimento, ativas somente com GBrain conectado.
- Testes ajustados para o fluxo com a pergunta nova; 9 passando.

## v0.2.3 — Instalação pelo Telegram e ciclo de vida

- Fluxo autorizado de instalação: a pessoa envia o repositório ao agente já
  conectado no Telegram; o agente segue `docs/instalar-pelo-telegram.md`.
- Registro privado extensível de conexões e rotinas (`scripts/modulos.py`):
  intenção `solicitado`/`desativado`; não executa integrações nem conecta contas.
- Migrações versionadas da base (`scripts/migrar.py`): backup dos arquivos
  afetados, idempotência, retomada após interrupção, reversão e conflitos
  explícitos. Perfil 300k opcional não é aplicado a instalações existentes.
- Templates não bloqueiam ajuda aguardando onboarding; automações opcionais
  (agenda, tarefas, YouTube e outras) permanecem escolha do dono.
- Testes de ciclo de vida (`tests/test_lifecycle.py`): instalação completa com
  retomada, escolhas, rollback, recuperação de migração interrompida, rejeição
  de caminhos privados/traversal. 9 testes passando no total.

## v0.2.2 — Revisão de onboarding, configuração e privacidade

- Onboarding deixa de solicitar tokens pelo Telegram e não anuncia backup sem
  sincronização/restauração implementadas. GitHub opcional registra intenção.
- Perguntas respeitam ordem, fuso é validado, pular funciona pelo wrapper;
  estado é gravado atomicamente com lock e acesso restrito.
- Inicialização preserva arquivos existentes mesmo em vault parcial, recusa
  caminhos dentro da base pública e prepara instrução no SOUL carregável.
- Configuração Hermes usa comandos nativos; não concatena YAML nem muda
  automaticamente modelo, aprovações ou STT. --yolo é escolha explícita.
- Perfil leve opt-in usa max_turns=25 e compactação nativa em 100 mil tokens
  com tail lean. Necessita benchmark em VPS limpa e versão compatível do Hermes.
- Atualização realiza fetch/fast-forward, verifica backup Git, recusa alterações
  locais/divergência. Migrações de runtime/personalização seguem pendentes.
- Capturas usam ID exato por hash, lock e escrita atômica; data inválida recusada.
- Documentação distingue mecanismos existentes, integrações planejadas e testes
  locais. Memória, SOUL e histórico enviados ao modelo não são somente locais.

Validação: testes unittest isolados e análise sintática. Sem teste real de bot,
OAuth, instalação completa em VPS ou migração entre releases nesta revisão.
