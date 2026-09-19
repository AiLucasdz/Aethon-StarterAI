
# Módulos de rotina — o que a base traz pronto

> Estes scripts vêm **generalizados** da instalação original: nenhum caminho
> pessoal fixado — tudo lê de variáveis de ambiente com defaults neutros.

## Variáveis de ambiente usadas

| Variável | Para que serve | Default |
|---|---|---|
| `VAULT_PATH` | pasta do vault Markdown do dono | `~/vault` |
| `HERMES_HOME` | home do runtime | `~/.hermes` |
| `YOUTUBE_CLIENT_SECRET` | caminho do client_secret OAuth do YouTube | vazio (módulo off) |

## Inclusos na base

| Script | Função | Quando ativa |
|---|---|---|
| `soul_sync` | projeta o soul versionado para o runtime | onboarding concluído |
| `diario_registrar` / `diario_commit` | registra capturas no diário do vault | sempre (módulo base) |
| `raw_capture` | captura bruta com message-id idempotente | sempre |
| `pessoa_registrar` | notas por pessoa no vault | onboarding pergunta se quer |
| `rotina_processar_resposta` | processa respostas às rotinas sem duplicar | se houver rotinas |
| `rotina_tracking` | tracking de rotinas ativas | se houver rotinas |
| `briefing_data` | dados calculados no fuso do dono | se briefing ativado |
| `transcricao_youtube` | transcrição de vídeo público (fiel) | dono pedir |
| `x_resumo` | resumo de X/Twitter | se módulo X ativado |
| `youtube_oauth` / `youtube_relatorio` | analytics do canal do dono | se módulo YouTube ativado |
| `context_pack` | pacote de contexto por entidade | módulo base |

## Não inclusos (específicos da instalação original)

- `fathom_*` (controle e keepalive OAuth do Fathom) — entra como módulo
  opcional "Reuniões" numa release futura; exigiria conta Fathom do dono.
- `test_*` — testes da instalação original, úteis como exemplos em `examples/`.
- `resumo_matinal` — substituído pelo briefing configurável.

## Regra para novos módulos

Nenhum script da base pode conter caminho absoluto de usuário, e-mail, ID de
conta ou token. Tudo via variável de ambiente com default neutro — o
`scripts/update.sh` falha se encontrar algo.
