# Bloco para o AGENTS.md da instalacao (gateway)

> Referência para instalação manual. O inicializador atual prepara o bloco no
> SOUL automaticamente; não é necessário duplicá-lo no AGENTS.md. Use o mesmo
> HERMES_HOME e VAULT_PATH da instalação ao invocar o script.

## Onboarding pendente (remover este bloco quando concluido)

Quando o dono quiser iniciar ou retomar a configuração, executar:

```bash
python3 {{BASE_DIR}}/scripts/gateway_hook.py
```

- Se a saida comecar com `ONBOARDING_ATIVO <chave>`: faça a pergunta do script
  se o dono estiver respondendo à configuração. Quando o dono
  responder, chame de novo com `--responder <chave> "resposta do dono"` e
  apresente a proxima pergunta (ou a conclusao).
- Se o dono disser "pular"/"depois": chame com `--pular <chave>` e siga o fluxo.
- Se a saida for `ONBOARDING_CONCLUIDO`: remova este bloco do AGENTS.md e
  responda a mensagem do dono normalmente.

Regras durante o onboarding:
- Ajude com pedidos de outro assunto; retome a configuração depois, sem obrigar
  a concluir o questionário. Nenhuma integração é requisito para uso.
- NUNCA improvise as perguntas — use exatamente o texto do script.
- NUNCA registre o token do GitHub em mensagem, vault ou soul.
- O nome do agente (primeira resposta) passa a ser como voce se apresenta.
