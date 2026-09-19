# Recuperação por turno

Plugin Hermes com `pre_llm_call` e `ctx.call_mcp`: usa o cliente MCP existente,
sem subprocesso GBrain ou LLM próprio. Compatibilidade exigida: Hermes com esses
pontos de extensão. Outros agentes leem SOUL/AGENTS e o contrato; precisam de
adaptador próprio para recuperação automática e não devem fingir que este hook roda.

Instale com `scripts/ativar-memoria.py`. Perfil, vault e dono do DM são configuração
privada, nunca valores deste repositório. CLI do perfil e DM confirmado no SQLite
recebem contexto; grupos, cron, subagentes, confirmações breves e slash não.

Busca local em AGENTS, decisões e lições atuais, mais recall GBrain (1.800 tokens
estimados pelo servidor, timeout 6s). Até dois trechos locais, três remotos e
6.000 caracteres totais, com prioridade para fonte atual. Não é índice completo
do vault. Sem resultados não acrescenta texto; erro remoto preserva busca local.
O Hermes pode persistir `api_content` para replay: o custo depende do histórico.
Logs guardam apenas contagens/tempo/tamanho, não consultas ou conteúdo pessoal.

Captura é semântica pelo agente, conforme `agent/memoria.md`, não um detector de
palavras que escreve fatos. Não há cache local obsoleto, cron ou banco adicional.

Se houver contexto irrelevante recorrente, vazamento entre escopos ou latência
inaceitável, use `hermes plugins disable aethon-memory` e recarregue fora do turno
ativo. Investigue preservando GBrain e as fontes; não apague a memória.
