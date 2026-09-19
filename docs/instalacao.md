
# Instalação

> **A instalação da VPS + Hermes + Telegram será ensinada em vídeo pelo criador
> deste template.** O vídeo cobre tudo antes de você chegar ao Telegram, onde o
> onboarding do agente começa.

## O que o vídeo cobre

1. Contratar VPS (recomendação: KVM 1 — [Hostinger, link de indicação](https://www.hostinger.com/br?REFERRALCODE=O23ELLUCA0ZD))
2. Acessar por SSH
3. Instalar o Hermes Agent (mecanismo oficial: https://hermes-agent.nousresearch.com/docs)
4. Configurar modelo no OpenRouter (GLM ou DeepSeek — confira IDs/preços atuais em https://openrouter.ai/models)
5. Criar o bot no BotFather e conectar o Telegram

## Depois do vídeo

Quando seu bot responder "oi" no Telegram, o **onboarding do agente começa
sozinho** — ele vai pedir o nome dele e quem é você:
ver [onboarding.md](onboarding.md).

No fim, o onboarding oferece (opcional, pode pular) o **backup do seu vault
num repositório privado do seu GitHub** — para isso ele vai pedir um token de
acesso com escopo `repo`. O token fica só no seu servidor (permissão 600) e o
repositório criado é privado.

## Referência escrita (oficial)

Docs do Hermes: https://hermes-agent.nousresearch.com/docs
