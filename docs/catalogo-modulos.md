# Catálogo e estado de implementação

Conectar conta e ativar rotina são escolhas separadas. Nenhuma conta externa ou
rotina é ativada pelo inicializador. Não prometer custo zero: plano externo,
embeddings e chamadas ao modelo podem ser cobrados.

O catálogo é ilustrativo e aberto. Agenda, Tasks e YouTube são escolhas
independentes. Também é possível usar tarefas locais sem conta externa e pedir
novas automações. O padrão inicial organiza a instalação sem restringir essas
escolhas. O agente deve implementar/testar cada capacidade antes de anunciá-la.

| Componente | Estado desta versão |
|---|---|
| Vault Markdown | Estrutura criada sem sobrescrever arquivos existentes |
| Onboarding | Script local + instrução no SOUL; validação Telegram real pendente |
| Escolhas de conexões/rotinas | Registro privado extensível em `scripts/modulos.py`; não executa integrações |
| Migração da base | Bloco gerenciado do SOUL e estado versionado; backup local e reversão com proteção contra conflitos |
| Memória nativa MEMORY/USER | Recurso do Hermes; conferir configuração efetiva |
| Honcho | Planejado/opcional; requer configuração própria e validação |
| GBrain | Planejado/opcional; não instalado por este template |
| Agenda/Tasks/Gmail | Planejado/opcional; conexão OAuth e testes não implementados |
| YouTube | Planejado/opcional; não herda canal ou OAuth de outro usuário |
| Fathom | Planejado/opcional; sem cron/timer instalado |
| X | Planejado/opcional para pesquisa/resumos; publicação não incluída |
| Backup privado | Migrações têm backup local; backup/import nativos do runtime testáveis em isolamento. Sincronização externa e recuperação integral do vault pendentes |

Honcho fornece contexto conversacional e representações; GBrain organiza,
relaciona e recupera conhecimento com fontes; memória nativa mantém notas curtas;
vault guarda registros duráveis. Não são equivalentes nem possuem sincronização
automática comprovada. Seus dados podem ser processados pelos serviços externos
configurados e pelo modelo, mesmo quando os arquivos ficam no servidor.

O registro atual separa `conexoes` e `rotinas`, com intenção `solicitado` ou
`desativado`; ausência significa nenhuma escolha. Não representa o estado real
de serviços externos. Desativar no registro exige também parar e verificar os
jobs no serviço responsável. Só conexão autenticada e consulta real permitem declarar
conectado. Só uma execução e entrega verificadas permitem declarar rotina ativa.
