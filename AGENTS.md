
# AGENTS.md — regras para agentes que trabalham neste template

Este repositório é um **template público** de agente pessoal. Nenhum dado
real de usuário pertence aqui.

## Regras absolutas

1. **Nunca** commite dados reais de usuário: nomes, tokens, chaves, contas,
   IDs de canal, memórias, conversas. A revisão deve cobrir histórico do git,
   arquivos ocultos e artefatos — .gitignore não é suficiente.
2. **Nunca** copie arquivos de uma instalação pessoal para cá. Reaproveite por
   seleção e generalização explícita (ex.: caminhos absolutos de usuário → caminho configurável).
3. O onboarding começa sempre pelo **nome do agente** e depois **quem é o dono**
   (ver docs/onboarding.md). Não inverta a ordem nem pule.
4. Conectar conta ≠ ativar rotina. Cada integração exige teste real antes de
   declarar sucesso.
5. IDs de modelo mudam: antes de editar docs que citam modelo/preço, conferir
   no OpenRouter na data. Nunca inventar ID.
6. Toda promessa de funcionalidade precisa de mecanismo real. Sem stubs
   disfarçados de features.

## Estrutura

- `agent/` — instrução de sistema do agente (o que ele é, como age)
- `templates/` — esqueletos com placeholders `{{...}}`
- `docs/` — guias para o dono e para o assistente de IA dele
- `scripts/` — instalação, atualização, migração
- `examples/` — exemplos fictícios (dados inventados claramente marcados)

## Ao criar release

- Changelog legível
- Verificar IDs de modelo recomendados
- Instruções de migração se houver mudança estrutural
- Revisão de privacidade do diff completo
