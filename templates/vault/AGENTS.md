
# AGENTS.md — regras deste vault

Este repositório é a memória durável de {{NOME_DO_AGENTE}}, agente de {{NOME_DO_DONO}}.

## Regra central

O agente não é dono da memória. A memória vive nestes arquivos Markdown.
Conferir fonte e data. Uma correção explícita atual do dono prevalece sobre uma nota antiga; atualize a nota com origem, sem transformar inferências em fatos.

## Hierarquia

- Cada pasta é a fonte única do seu assunto (identidade, projetos, tarefas...)
- Em conflito, o arquivo mais específico vence
- Não duplicar informação entre pastas; apontar para a fonte

## Como o agente registra

1. Consulte antes de agir e registre na fonte especializada, com origem e data
2. Use `00_INBOX/` se o destino estiver indefinido; consolide preservando origem
3. Compromissos ("prometi fazer X com Y") sempre citam pessoa e data
4. Dúvida ≠ fato: hipóteses ficam marcadas como hipóteses
5. Decisões gerais em `08_DECISOES/decisoes.md`; lições verificáveis em
   `09_AGENTES/licoes-operacionais.md`. Consulte assunto, estado e aplicação.
6. Confirme releitura e recuperação; se o índice falhar, diga qual camada foi salva.
7. Priorize desempenho, custo e clareza; evite duplicar código, notas e instruções.

## O que nunca entra aqui

- Senhas, tokens, chaves de API
- Documentos completos com dados pessoais sensíveis de terceiros
- Qualquer coisa que o dono não colocaria num repositório privado dele
