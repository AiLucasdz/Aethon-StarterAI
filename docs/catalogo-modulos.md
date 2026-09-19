# Catálogo e estado de implementação

Conectar conta e ativar rotina são escolhas separadas. Nenhuma conta externa ou
rotina é ativada pelo inicializador. Não prometer custo zero: plano externo,
embeddings e chamadas ao modelo podem ser cobrados.

| Componente | Estado desta versão |
|---|---|
| Vault Markdown | Estrutura criada sem sobrescrever arquivos existentes |
| Onboarding | Script local + instrução no SOUL; validação Telegram real pendente |
| Memória nativa MEMORY/USER | Recurso do Hermes; conferir configuração efetiva |
| Honcho | Planejado/opcional; requer configuração própria e validação |
| GBrain | Planejado/opcional; não instalado por este template |
| Agenda/Tasks/Gmail | Planejado/opcional; conexão OAuth e testes não implementados |
| YouTube | Planejado/opcional; não herda canal ou OAuth de outro usuário |
| Fathom | Planejado/opcional; sem cron/timer instalado |
| X | Planejado/opcional para pesquisa/resumos; publicação não incluída |
| Backup privado | Interesse registrado; sincronização/restauração não implementadas |

Honcho fornece contexto conversacional e representações; GBrain organiza,
relaciona e recupera conhecimento com fontes; memória nativa mantém notas curtas;
vault guarda registros duráveis. Não são equivalentes nem possuem sincronização
automática comprovada. Seus dados podem ser processados pelos serviços externos
configurados e pelo modelo, mesmo quando os arquivos ficam no servidor.

Estados futuros por módulo: off, solicitado, conectando, conectado, erro; rotinas
terão estado próprio. Só conexão autenticada e consulta real permitem declarar
conectado. Só uma execução e entrega verificadas permitem declarar rotina ativa.
