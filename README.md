# Aethon-StarterAI — base para seu agente pessoal

> Template público. Nenhum dado pessoal aqui — a configuração privada da sua
> instalação vive fora deste repositório (ver `docs/privacidade.md`).

## O que é

Uma base replicável de agente pessoal, construída sobre o
[Hermes Agent](https://hermes-agent.nousresearch.com/docs). Você instala na sua
VPS, conecta seu Telegram, escolhe o nome do seu agente e ativa gradualmente as
conexões que quiser.

**Estado: versão em revisão, sem validação completa em VPS/Telegram.** Veja [limites e desempenho](docs/performance.md).

**Seu agente, seu nome.** Durante o onboarding no Telegram, a primeira coisa
que o agente vai te pedir é:

1. **O nome dele** — você escolhe (exemplos: Argos, Jarvis, Sábi, como preferir).
2. **Quem é você** — nome, o que faz, o que o agente pode e não pode fazer por você.

Essas informações moldam a personalidade do agente (arquivo `soul` dele) e são
gravadas nos arquivos privados da sua instalação. Telegram, modelo e integrações podem processar as mensagens; armazenamento local não significa processamento exclusivamente local.

## Como funciona (visão geral)

```
Você (Telegram) ↔ Hermes (VPS) ↔ Modelo de IA (OpenRouter: GLM ou DeepSeek)
                        ↕
            Memória local (Markdown + índice)
                        ↕
      Conexões que VOCÊ ativar: Agenda, Tasks, Gmail, YouTube, Reuniões...
```

## Instalação

**A instalação (VPS + Hermes + Telegram) é ensinada em vídeo pelo criador.**
O link do vídeo ainda está pendente. Após instalar Hermes e parear o bot, execute
`bash scripts/iniciar.sh`. O onboarding é orientado por uma instrução no SOUL;
a validação real desse fluxo no Telegram ainda está pendente.

- Link de VPS recomendada: [Hostinger, código de indicação](https://www.hostinger.com/br?REFERRALCODE=O23ELLUCA0ZD)
- Visão geral escrita: [docs/instalacao.md](docs/instalacao.md)
- Conexões opcionais: [docs/catalogo-modulos.md](docs/catalogo-modulos.md)
- Memória (vault): [docs/vault.md](docs/vault.md) — Obsidian é opcional; o vault é só Markdown no seu servidor

## Conexões opcionais — adaptadores ainda pendentes

Nada é ativado por padrão. Após o onboarding, o agente te pergunta o que você
quer ativar, explicando custo, benefício e requisitos de cada uma:

| Conexão | Para que serve |
|---|---|
| Google Agenda + Tasks | Compromissos, tarefas, planejamento diário |
| Gmail | Leitura e envio de e-mails (com confirmação) |
| YouTube | Análise do seu próprio canal |
| Reuniões (Fathom) | Resumos e acompanhamento de decisões |
| X/Twitter | Pesquisa e resumos, quando implementado e autorizado |

Credenciais nunca são pedidas no chat — sempre por entrada segura ou OAuth.

## Para quem é

- Quem quer um assistente pessoal com memória, rodando no seu próprio servidor
- Quem quer controlar exatamente quais dados saem de casa
- Desenvolvedores que querem fazer fork e melhorar

## Licença e garantias

- Sem garantias — leia o código antes de rodar no seu servidor
- Custos da sua conta: VPS + API do modelo (nada incluso aqui é grátis de verdade)

---

*Este projeto é mantido por forks da comunidade. A base atualizável acompanha
releases do upstream; suas personalizações ficam em arquivos que o sistema
sabe preservar durante atualizações (ver `docs/atualizacoes.md`).*
