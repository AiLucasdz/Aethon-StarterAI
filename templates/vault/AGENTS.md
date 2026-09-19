
# AGENTS.md — regras deste vault

Este repositório é a memória durável de {{NOME_DO_AGENTE}}, agente de {{NOME_DO_DONO}}.

## Regra central

O agente não é dono da memória. A memória vive nestes arquivos Markdown.
Se a memória interna do agente divergir dos arquivos, **os arquivos vencem**.

## Hierarquia

- Cada pasta é a fonte única do seu assunto (identidade, projetos, tarefas...)
- Em conflito, o arquivo mais específico vence
- Não duplicar informação entre pastas; apontar para a fonte

## Como o agente registra

1. Toda captura vai primeiro em `00_INBOX/` com origem e data
2. Consolidação move conhecimento para a pasta certa, preservando origem
3. Compromissos ("prometi fazer X com Y") sempre citam pessoa e data
4. Dúvida ≠ fato: hipóteses ficam marcadas como hipóteses

## O que nunca entra aqui

- Senhas, tokens, chaves de API
- Documentos completos com dados pessoais sensíveis de terceiros
- Qualquer coisa que o dono não colocaria num repositório privado dele
