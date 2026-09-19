# Skills incluídas no fluxo de instalação

## Diagramas — Archify

Fonte: [tt-a1i/archify](https://github.com/tt-a1i/archify), licença MIT.
O pacote foi usado para gerar e validar o diagrama público. O scanner Hermes
classificou-o como `caution` (tamanho, CLI, fontes embutidas e Unicode); isso
pode interromper a instalação até revisão e autorização do responsável.
A revisão inicial usou o commit `72c750bb070d95171dbb2244e5b62b1b7da69c12`.
A distribuição usa o gerenciador nativo do Hermes; não copia a skill inteira
para o template nem mantém um instalador paralelo.

No perfil identificado durante a instalação, confira a lista de skills. Se
Archify já existir, preserve-a e valide seus requisitos. Caso contrário:

```bash
# HERMES_HOME deve apontar para o perfil alvo, fora do checkout.
hermes skills install tt-a1i/archify/archify --yes
```

O gerenciador busca a versão upstream atual, faz sua análise de segurança e
registra a origem. Compare a revisão resolvida com a auditada acima; mudanças
exigem nova revisão antes de usar. Se o scanner bloquear, informe achados e revisão exata ao responsável. Exceção
   somente com autorização explícita após essa revisão; nunca como padrão do template.
Confirme o resultado: código de saída sozinho não basta para provar instalação.

1. Conferir `hermes skills list` e a ferramenta nativa `skills_list`/`skill_view`.
2. No diretório instalado, executar `node bin/archify.mjs doctor`; requer Node.js
   18+ (preferir uma versão ainda suportada). Browser é necessário para a revisão
   visual automatizada, não para todo uso do agente.
3. Gerar um diagrama de teste sem dados pessoais, validar e abrir a saída antes
   de anunciar geração funcionando.

Uso sob demanda para arquitetura, processos, sequências e fluxos. As instruções
completas não entram no SOUL nem em toda conversa; os diagramas são gerados
localmente. Dados de uma conversa ainda podem ser processados pelo modelo.
Não publique diagramas empresariais ou pessoais sem autorização.

O JSON e HTML em `docs/assets/` representam apenas este template público.
