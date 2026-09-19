# Segundo cérebro: instalação padrão

O agente já é um segundo cérebro. Vault, memória nativa disponível e GBrain fazem
parte do fluxo; só Honcho pode ser recusado no onboarding. Falta de requisito
significa configuração pendente, não uma versão alternativa do agente.

| Camada | Responsabilidade |
|---|---|
| Markdown | Fonte durável: perfil, projetos, decisões e lições com origem |
| MEMORY/USER nativas | Mapa e convenções curtas / perfil estável, via ferramenta do Hermes |
| GBrain | Recuperação com fontes; índice não substitui a autoridade do Markdown |
| Honcho | Continuidade conversacional adicional; conclusões são revisáveis |

## GBrain incluído

Após `iniciar.py`, execute `ativar-memoria.py` com o mesmo `HERMES_HOME` e
`VAULT_PATH`, informando `--telegram-owner ID` quando houver Telegram. O script:

1. Confirma o perfil pelo CLI Hermes; guarda backup privado da configuração.
2. Preserva um MCP `gbrain` já configurado, sem abrir sua base em outro processo.
3. Se não existir MCP, usa GBrain instalado ou instala `github:garrytan/gbrain#v0.46.12.3` (versão validada nesta revisão)
   pelo Bun. O pacote homônimo do npm não deve ser usado. Se Bun faltar, instale
   pelo [guia oficial](https://bun.sh/docs/installation) e retome.
4. Cria base isolada em `<HERMES_HOME>-gbrain/.gbrain` (diretório irmão do runtime), com PGLite, sem embeddings,
   modo conservative, e importa o vault sem chamadas de embedding.
5. Registra MCP com a superfície `verbs` e habilita `aethon-memory` via comandos
   nativos. Não troca modelo, compressão, contas, aprovações ou cron.

A opção inicial sem chave permite instalar a memória sem pedir credenciais no
chat. Começa com busca textual, não busca semântica. Quando houver credencial
adequada do dono, configure embeddings nativamente e valide custo/recuperação;
reutilize configuração existente sem reindexar ou mudar modelo por conta própria.
Referência: [GBrain oficial](https://github.com/garrytan/gbrain), que orienta começar
sem chave e acrescentar busca semântica quando necessária. As versões mudam:
confira compatibilidade com `init --no-embedding`, `serve --surface verbs` e o
contrato `remember/recall` antes de atualizar uma instalação.

A base GBrain fica fora do runtime: arquivos internos do PGLite podem ter datas
incompatíveis com o ZIP nativo do Hermes, além de exigir cópia consistente.
O backup Hermes não cobre essa base nem o vault externo. Use exportação/snapshot
próprio com a base parada e teste restauração antes de prometer backup completo.
Não copie um PGLite aberto nem crie outro processo para fazer o backup.

### Validar no consumidor

Recarregue o gateway fora do turno ativo. No próximo turno, verifique ferramentas,
texto recuperado e origem. Use uma decisão real do onboarding para testar captura:
registre no Markdown, `remember` com entidade/tipo/proveniência e `recall` pelo MCP.
Repita a captura consultando primeiro entidade/texto/origem e reaproveite o ID
existente: sem embeddings a escrita pode não deduplicar sozinha. Em sessão nova, pergunte sem
indicar o arquivo e confira aplicação na resposta. Não simule fatos do dono.

Não rode `gbrain import`, `doctor`, outro servidor ou `hermes mcp test` contra o
mesmo PGLite enquanto o gateway o utiliza. Para manutenção, drene e pare o
consumidor, execute os comandos e reinicie; em conversa ativa use o MCP já aberto.
`hermes mcp test` só é adequado quando não há outro processo usando essa base.
Não declarar sucesso pelo código de saída/ID sem inspecionar resposta.

`private` pode gravar e não voltar pelo MCP: nas versões com leitura remota
restrita a `world`, esse escopo permite acesso aos consumidores da mesma base.
Não torna dados públicos na internet. Confira isolamento antes de usá-lo; não
promova registros anteriores em lote. Ver [contrato de memória](../agent/memoria.md).

## Honcho oferecido no onboarding

O onboarding pergunta se pode configurar Honcho, explica serviço externo/custo
sem pedir chave e aceita recusa. Com aceitação, o agente deve executar o setup,
não apenas anotar intenção. Se já houver configuração, validar e preservar.

1. Use `hermes memory setup honcho` no terminal seguro para credenciais do dono.
   Sem interação segura disponível, explique o único passo externo necessário e
   retome após concluído; nunca peça chave pelo Telegram.
2. Confira peers existentes. Use `hermes honcho peer --user <identidade>` para
   definir a identidade CLI apropriada. Preserve o histórico e o isolamento de
   Telegram/CLI/outros agentes; não crie peer vazio para mascarar um erro.
3. Confira provider efetivo, flags de memória nativa e modo de observação.
   Não troque um provedor existente silenciosamente nem altere relações entre peers.
4. `hermes honcho status` precisa retornar dados, não só `OK`. Um aviso como
   `Peer data unavailable` é falha. Verifique contexto no consumidor em nova sessão
   e novas gravações separadamente. Não misture acesso com qualidade das conclusões.

Sem Honcho, o segundo cérebro continua com GBrain, vault e memória nativa.
Não há sincronização contínua entre camadas nem garantia de captura espontânea:
a execução segue o contrato e precisa ser observada no uso real. Não são
ativadas rotinas de enriquecimento ou chamadas de síntese por padrão.
