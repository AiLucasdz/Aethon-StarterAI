# Onboarding — o que o agente pergunta na primeira conversa

> Template. O fluxo abaixo roda no Telegram, logo após o dono parear a conta.
> Objetivo: personalizar o agente em minutos, sem questionário interminável.
> Tudo pode ser pulado e retomado depois — nada é obrigatório.

## Princípios

- **Primeira pergunta: o nome do agente.** É o que o dono decide primeiro.
- Depois, **quem é o dono** — o suficiente para o agente ser útil.
- Gradual: perguntar um pouco, usar, voltar a perguntar depois.
- Pular ≠ recusar. O agente funciona mesmo sem responder tudo.
- Só se pula a pergunta **atual** (não dá para pular fora de ordem) — mantém o fluxo previsível.
- Tudo salvo **localmente**, no `soul` do agente. Nada sai do servidor.

## Fluxo

### 1. Nome do agente

```
Oi! Sou seu agente pessoal, rodando no SEU servidor.
Antes de tudo: como você quer me chamar?
(Pode ser Argos, Jarvis, Sábi... ou o que vier à cabeça)
```

- O nome escolhido vira o `agent_name` no soul e é usado em todas as mensagens.
- Sem resposta → sugestão neutra temporária ("assistente").

### 2. Quem é o dono (base do soul pessoal)

```
Prazer, {nome}! Agora me conta rapidinho sobre você — isso me ajuda
a responder do jeito certo:

1. Como você quer ser chamado?
2. O que você faz? (trabalho/projeto principal)
3. O que você mais quer que eu faça por você? (até 3 coisas)
4. Tem algo que eu NUNCA devo fazer?
```

Salva em `soul` como: identidade do dono, foco atual, desejos, limites.

### 3. Preferências de estilo (opcional, pode pular)

```
Como prefere minhas respostas?
- Curtas e diretas
- Com contexto e explicação
- Tanto faz, você decide
```

### 4. Fuso horário e idioma

```
Em que fuso você está? (ex.: America/Sao_Paulo)
Idioma principal: português? (ou outro)
```

### 5. Fim do básico — anuncia as conexões

```
Pronto, {nome_do_agente} está no ar! 🚀
Deixa eu te contar o que posso conectar quando você quiser:

📅 Agenda + Tasks — compromissos e planejamento
📧 Gmail — ler e enviar e-mails (com sua confirmação)
🎬 YouTube — análise do seu canal
🎙️ Reuniões — resumos automáticos
𝕏 — postar e monitorar

Quer ativar alguma agora? (ou diga "depois" e me usa já)
```

**Regra central: conectar conta ≠ ativar rotina.** Se o dono ativar uma
conexão, o agente pergunta separadamente: frequência, horário, destino e
intenção. Cada integração é **testada de verdade** antes de o agente declarar
que está funcionando.

### 6. Backup no GitHub (opcional)

```
Quer que eu faça backup do seu vault num repositório PRIVADO do seu GitHub?
Se sim, me manda um token de acesso:
1. https://github.com/settings/tokens/new
2. Marque só 'repo'
3. Gere e cole aqui
⚠️ O repo que eu criar será PRIVADO (só você vê) e o token fica salvo
só neste servidor, com permissão restrita. Ou digite 'pular'.
```

O que o agente faz com o token:
- **Valida na API** na hora (token errado → pede de novo ou aceita "pular")
- Salva em `~/.git-credentials` com permissão **600**, fora de qualquer repositório
- Cria o repositório **PRIVADO** `meu-vault-privado` para o backup do vault
- O token **nunca** vai para o vault, nem para o soul, nem para o GitHub

## O que fica salvo e onde

| Informação | Arquivo | Sobe pro GitHub? |
|---|---|---|
| Nome do agente | soul local | ❌ nunca |
| Identidade do dono | soul local | ❌ nunca |
| Preferências | soul local | ❌ nunca |
| Conexões ativadas | config local | ❌ nunca |
| Token do GitHub | `~/.git-credentials` (perm. 600) | ❌ nunca |
| Backup do vault | repo PRIVADO do dono | 🔒 só o dono vê |

O template público contém apenas o **esqueleto vazio** desses arquivos, com
placeholders `{{...}}`.
