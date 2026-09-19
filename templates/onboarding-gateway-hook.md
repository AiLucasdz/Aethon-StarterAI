# Bloco para o AGENTS.md da instalacao (gateway)

> Este bloco e colado no AGENTS.md que o gateway le, durante a instalacao,
> ENQUANTO o onboarding estiver pendente. Ao concluir, o proprio agente o
> remove (o script imprime ONBOARDING_CONCLUIDO).

## Onboarding pendente (remover este bloco quando concluido)

Antes de responder QUALQUER mensagem do dono, executar:

```bash
python3 {{BASE_DIR}}/scripts/gateway_hook.py
```

- Se a saida comecar com `ONBOARDING_ATIVO <chave>`: NAO responda a mensagem
  do dono ainda. Faca a pergunta que o script imprimiu. Quando o dono
  responder, chame de novo com `--responder <chave> "resposta do dono"` e
  apresente a proxima pergunta (ou a conclusao).
- Se o dono disser "pular"/"depois": chame com `--pular <chave>` e siga o fluxo.
- Se a saida for `ONBOARDING_CONCLUIDO`: remova este bloco do AGENTS.md e
  responda a mensagem do dono normalmente.

Regras durante o onboarding:
- NUNCA improvise as perguntas — use exatamente o texto do script.
- NUNCA registre o token do GitHub em mensagem, vault ou soul.
- O nome do agente (primeira resposta) passa a ser como voce se apresenta.
