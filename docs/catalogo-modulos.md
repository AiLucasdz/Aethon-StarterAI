
# Catálogo de módulos (conexões opcionais)

> Nada ativado por padrão. O dono escolhe no Telegram; cada ativação é
> **testada de verdade** antes de o agente dizer que funciona.
> Conectar conta ≠ ativar rotina: frequência/horário/destino são perguntas separadas.

## Base (sempre incluída)

| Módulo | Função | Requisito |
|---|---|---|
| Conversa Telegram | canal principal | bot já conectado no vídeo de instalação |
| Memória local (Markdown/vault) | notas duráveis do dono — a fonte de verdade | nada extra |
| Memória de recuperação (índice vetorial) | achar por assunto/entidade | roda local |
| Contexto relacional (Honcho) | como o dono gosta de conversar, padrões de sessão | chave Honcho (nível gratuito cobre) |
| Índice de conhecimento (GBrain) | recuperação por entidade sobre o vault | roda local |

## Opcionais

| Módulo | Para que serve | Requisito | Custo extra |
|---|---|---|---|
| **Agenda Google** | compromissos, planejamento diário, briefing matinal | OAuth Google | 0 |
| **Google Tasks** | lista de tarefas do dono | OAuth Google | 0 |
| **Gmail** | ler/separar/enviar e-mails (envio exige confirmação) | OAuth Google | 0 |
| **YouTube (próprio canal)** | analytics do canal do dono | OAuth Google | 0 |
| **Reuniões (Fathom)** | resumo e compromissos de reuniões gravadas | conta Fathom | plano Fathom |
| **X/Twitter** | postar e monitorar | chave API própria | API paga |
| **Transcrição de vídeo** | transcrever YouTube de terceiros | serviço externo | 0 (com limites) |

## Estados possíveis

- `off` (padrão) — código não executa, nem aparece no onboarding como ativo
- `conectado` — credenciais OK, nenhuma rotina rodando
- `ativo` — pelo menos uma rotina escolhida pelo dono, testada

## Regra do onboarding

Ao ativar qualquer módulo, o agente explica: utilidade, requisitos, custo e
quais dados saem do servidor. Só depois pede a conexão. E pergunta em seguida
quais rotinas (se alguma) o dono quer.
