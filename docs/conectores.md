# Conectores reais — Agenda, Tasks, Gmail, YouTube, Fathom, X

Estado: nenhum conector está ligado por padrão. O registro (`scripts/modulos.py`)
marca **intenção**; esta página define como cada conexão é feita e verificada
quando o dono pedir. Regra permanente: **conectar conta não ativa rotina**, e
nada é anunciado como funcionando sem consulta real ao serviço.

Credenciais sempre do dono, sempre por fluxo seguro (OAuth no terminal ou
arquivo de credencial local). Nunca token no chat, nunca copiar credencial de
outra instalação, nunca herdar OAuth de outro usuário.

## Google (Agenda, Tasks, Gmail) — via skill google-workspace do Hermes

O Hermes traz a skill `productivity/google-workspace` com setup OAuth guiado,
não interativo, feito passo a passo entre o agente e o dono:

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"

$GSETUP --check                # 1. auth já válida? sai sem fazer nada
$GSETUP --client-secret /caminho/client_secret.json   # 2. arquivo do Google Cloud Console do DONO
$GSETUP --auth-url             # 3. o agente envia a URL ao dono
$GSETUP --auth-code CODIGO     # 4. o dono autoriza e cola o código; o agente troca pelo token
$GSETUP --check                # 5. verificar de novo — só então declarar conectado
```

Depois, uso pelo `google_api.py` da mesma skill (`gmail search`, `calendar
list`, etc.). Verificação de cada serviço antes de anunciar:

- Gmail: `gapi gmail search "is:unread" --max 1` retorna resultado ou vazio sem erro
- Agenda: `gapi calendar list` lista calendários reais
- Tasks: consulta real da lista do dono

Requisitos do dono: projeto no Google Cloud Console com OAuth client (Desktop)
e escopos de Gmail/Calendar/Tasks. O template não cria projeto nem pede
client_secret no chat.

Alternativa com MCP: `hermes mcp install` do catálogo oficial quando houver
entrada Google adequada; ou MCP local (workspace-mcp) com as credenciais do
dono. Testar com `hermes mcp test <nome>`.

## YouTube

Dois usos distintos, com credenciais diferentes:

1. **Ler/transcrever vídeos públicos** — skill `media/youtube-content` do
   Hermes. Sem OAuth do canal do dono; atenção à privacidade de vídeos
   privados/não listados (ver docs/privacidade.md).
2. **Gerir o canal do dono** (uploads, métricas) — precisa OAuth do canal com
   escopo próprio, feito pelo fluxo seguro no terminal. Não implementado como
   script no template; o agente configura quando o dono pedir, usando a
   mesma disciplina do Google (URL → código → token → check).

## Fathom (reuniões)

O catálogo de MCPs do Hermes pode ter entrada Fathom; senão, API key própria
do dono em variável de ambiente (`~/.hermes/.env`), nunca no chat. Verificar
com consulta real (listar uma reunião) antes de declarar conectado.

## X (Twitter)

Leitura/pesquisa via skill `xurl` do Hermes (API key do dono). Publicação só
com confirmação explícita por post. Não incluir credenciais no template.

## Fim a fim: o que "conectado" exige

Para cada conector, o ciclo é o mesmo:

1. Dono pede → registrar intenção (`modulos.py solicitar conexao <id>`)
2. Agente explica custo/escopo/efeitos e pede confirmação da conexão
3. Credencial do dono por fluxo seguro (OAuth/terminal/env local)
4. **Consulta real** ao serviço (exemplos acima) — exit 0 e resposta não vazia
5. Registrar estado real no registro do dono e avisar o que ficou pendente
6. Rotinas: só com pedido explícito separado (escopo, frequência, destino),
   e depois testar execução + entrega antes de declarar ativa

Nunca: anunciar conectado sem o passo 4; ligar rotina como efeito colateral
da conexão; usar o bot de produção para testar instalação alheia.
