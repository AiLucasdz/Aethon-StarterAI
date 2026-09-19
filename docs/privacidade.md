
# Privacidade — o que fica no seu servidor e o que sai dele

## Regra de ouro

**Sua instalação é sua.** Este repositório público não contém e nunca conterá
dados dos usuários. E sua instalação privada nunca deve virar pública.

## O que sai do seu servidor

| Dado | Vai para | Quando |
|---|---|---|
| Mensagens suas | Provedor do modelo (OpenRouter) | a cada conversa |
| Suas mensagens | Telegram | sempre (é o canal) |
| Consultas de web | sites consultados | quando o agente pesquisa |

## O que NÃO sai do seu servidor

- Suas memórias e notas (Markdown local)
- Identidade do soul (seu nome, seus limites)
- Tokens e credenciais de conexões
- Histórico de conversas do Telegram

## Antes de forkar ou publicar qualquer variação

A revisão de privacidade deve abranger: conteúdo visível, histórico do git,
arquivos ocultos, artefatos compilados e logs. **.gitignore não basta** —
dados podem estar no histórico de commits. Se seu fork derivou de uma
instalação pessoal, o caminho seguro é começar de um checkout limpo do
template, não de dentro da instalação.

## Credenciais

- Nunca em chat do Telegram. Sempre OAuth ou entrada segura no servidor.
- Nunca em arquivos versionados. `.env` local + variáveis de ambiente.
- Revisão anual (ou por suspeita) de quais serviços têm acesso a quê.
