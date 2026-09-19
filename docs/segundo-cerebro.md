# Segundo cérebro: GBrain + Honcho

O template pode operar como segundo cérebro em quatro camadas complementares:

| Camada | O que guarda | Onde vive |
|---|---|---|
| Vault Markdown | Registros duráveis (decisões, diário, pessoas) | Seu servidor, em Markdown |
| Memória nativa MEMORY/USER | Notas compactas e estáveis | Recurso do Hermes |
| GBrain | Conhecimento com relações, busca semântica e síntese com fontes | Seu servidor (PGLite local) + API de embeddings |
| Honcho | Contexto conversacional e representação do dono ao longo das sessões | Serviço Honcho (nuvem) |

Nenhuma é ligada por padrão. Conectar não ativa rotinas. Custo: embeddings e
planos externos são cobrados — cada serviço apresenta preço antes da escolha.

## Honcho (contexto conversacional)

O Hermes já traz Honcho como provedor de memória nativo. Para ativar:

1. Crie conta em https://app.honcho.dev e gere sua API key.
2. Grave a chave fora do repositório:
   `hermes memory setup honcho` (fluxo nativo, disponível antes de ativar o
   provedor; mantém credenciais na configuração privada do Hermes).
3. Dê um peer ao seu usuário (como o agente deve chamar você na memória):
   `hermes honcho peer --user <nome>`.
   Em instalação existente, confira `hermes honcho peers` e preserve a identidade
   que já possui o histórico. Identidades do Telegram e CLI podem ser distintas;
   não una usuários ou agentes de trabalho automaticamente.
4. Verifique `hermes honcho status`: o peer deve estar definido e a leitura de
   seus dados deve funcionar. A saída final `OK` sozinha não basta: algumas
   versões também imprimem `Peer data unavailable` antes dela. Abra uma nova
   sessão e confira a inicialização e recuperação de contexto sem esse erro.

Referência: [documentação oficial do Hermes](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/honcho.md).

Sem chave, a memória nativa local (MEMORY/USER) segue funcionando.

## GBrain (conhecimento, relações e síntese)

GBrain é open source (MIT, github.com/garrytan/gbrain), roda local em PGLite e
precisa de Bun e de uma API key de embeddings.

### Instalação

```bash
# 1. Bun (runtime necessário)
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"

# 2. GBrain — SEMPRE do GitHub. O pacote 'gbrain' do npm é OUTRO projeto.
bun install -g github:garrytan/gbrain
gbrain --version   # deve imprimir uma versão
```

### Chave de embeddings

A stack padrão usa Voyage (`voyage-4` + rerank; uma chave cobre os dois).
OpenAI é alternativa. Sem chave nenhuma, a busca por palavra-chave continua
funcionando — só sem busca semântica.

```bash
export VOYAGE_API_KEY=pa-...   # ou OPENAI_API_KEY=sk-...
```

Guarde a chave no shell profile ou em `~/.gbrain/config.json` (arquivo), nunca
em mensagens de chat e nunca no repositório.

### Criação do cérebro e modo de busca

```bash
gbrain init          # cria o cérebro em PGLite, sem servidor
gbrain doctor --json # todos os checks devem passar
```

O `gbrain init` aplica um modo de busca automático (tokenmax). O custo por
consulta varia até 25x entre modos — escolha consciente, não aceite o padrão em
silêncio. Valores de referência do guia oficial (10 mil consultas/mês):

| Modo | Haiku-class ($1/M) | Sonnet-class ($3/M) | Opus-class ($5/M) |
|---|---|---|---|
| conservative | $40/mês | $120/mês | $200/mês |
| balanced | $100/mês | $300/mês | $500/mês |
| tokenmax | $200/mês | $600/mês | $1.000/mês |

- `conservative` — 4K de contexto, sem expansão LLM, 10 chunks. Volume alto/custo baixo.
- `balanced` — 12K, sem expansão, 25 chunks. Equilíbrio comum.
- `tokenmax` — sem limite, expansão LLM ligada, 50 chunks. Modelos frontier.

Para trocar: `gbrain config set search.mode <modo>` e confirme com
`gbrain search modes`. O instalador deve apresentar esta matriz e perguntar
antes de prosseguir — não aceitar o padrão em silêncio.

### Registro no Hermes (MCP)

```bash
printf 'Y\n' | hermes mcp add gbrain --env GBRAIN_HOME=$HOME \
  --connect-timeout 60 --command $(which gbrain) --args serve
hermes mcp test gbrain   # verificação real; o add sozinho não prova conexão
```

Reinicie o gateway depois de registrar. A partir daí o agente ganha os verbos
`gbrain remember / recall / query` — captura com entidade e tipo, recuperação
com fontes.

### Primeira indexação

```bash
gbrain import "$VAULT_PATH" --no-embed   # importa o vault em Markdown
gbrain embed --stale                     # gera embeddings
gbrain stats                             # confere páginas e links
```

## O que NÃO esperar

- Nenhuma sincronização automática entre as camadas: o vault não indexa o
  GBrain sozinho, o Honcho não lê o vault. A captura que alimenta cada camada
  é comportamento do agente, definido nas instruções dele.
- Dados locais não saem do servidor exceto pelos serviços que você conectar
  (modelo, embeddings, Honcho). Revise `docs/privacidade.md`.
- O onboarding pergunta se você quer cada camada; pular não deixa a instalação
  incompleta — o agente funciona com vault + memória nativa.

## Checklist do instalador (agente)

Ao pedir GBrain/Honcho para o dono, execute e verifique cada passo antes de
declarar ligado:

- [ ] Bun instalado (`bun --version`)
- [ ] `gbrain --version` responde (instalação via github:garrytan/gbrain)
- [ ] Chave de embeddings gravada em arquivo, não em chat
- [ ] `gbrain init` + `gbrain doctor --json` sem falhas
- [ ] Modo de busca escolhido pelo dono após ver a matriz de custo
- [ ] `hermes mcp test gbrain` conectado + gateway reiniciado
- [ ] `hermes honcho status` conectado + peer do usuário definido
- [ ] `gbrain stats` mostra o vault importado
