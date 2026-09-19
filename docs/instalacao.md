
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

Link do vídeo ainda pendente. Com Hermes e bot já configurados, execute
`bash scripts/iniciar.sh` usando os caminhos privados da instalação, seguido de
`python3 scripts/ativar-memoria.py --telegram-owner ID_DO_DONO` para GBrain e
recuperação. Pelo Telegram, peça ao agente para seguir
[instalar-pelo-telegram.md](instalar-pelo-telegram.md). Veja
[onboarding.md](onboarding.md) para carregamento do SOUL e limites da integração.
O onboarding não coleta token GitHub; registra somente interesse em backup.

## Referência escrita (oficial)

Docs do Hermes: https://hermes-agent.nousresearch.com/docs
