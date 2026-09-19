# Vault — fontes privadas em Markdown

O vault é uma pasta fora do checkout público. Obsidian é um leitor/editor opcional.
`VAULT_PATH` define o destino; o padrão é `~/vault`.

| Pasta | Conteúdo |
|---|---|
| `00_INBOX` | Material recebido que ainda precisa de organização |
| `01_IDENTIDADE` | Perfil e preferências informados pelo dono |
| `02_SAUDE_E_CORPO` | Informações de saúde compartilhadas, sem inferir fatos |
| `03_CARREIRA_E_NEGOCIOS` | Projetos e trabalho |
| `04_FINANCAS` | Contexto financeiro escolhido pelo dono, sem credenciais |
| `05_TAREFAS` | Contexto de tarefas; não instala sincronização com Tasks |
| `06_IA_E_AUTOMACOES` | Automações e materiais para consulta/estudo |
| `07_DIARIO` | Capturas pessoais quando pertinentes, sem check-in obrigatório |
| `08_DECISOES` | Decisões confirmadas, motivo, origem e revisão |
| `09_AGENTES` | Lições operacionais com evidência e instruções dos agentes |
| `10_PESSOAS_E_RELACOES` | Contexto compartilhado de pessoas e relações |
| `90_EXPORTS` | Contexto portátil, selecionado antes de compartilhar |

## Como a informação é usada

`AGENTS.md` é o mapa. O [contrato](../agent/memoria.md) orienta identificar o que
merece registro, salvar na fonte apropriada e recuperar por relevância antes de
agir. Não é preciso copiar toda mensagem para inbox nem criar uma lição por turno.
Material de estudo é para o dono consultar; não autoriza aplicar seu conteúdo ao agente.

O plugin recupera regras, lições e decisões locais e consulta GBrain pelo MCP
nativo. A instalação nova usa busca textual; embeddings são configuração extra.
Arquivos canônicos prevalecem sobre resumos desatualizados. GBrain ajuda a localizar;
Honcho, quando configurado, complementa a continuidade. Nenhum cron de consolidação
ou sincronização com serviços externos é criado por esta estrutura.

## Backup opcional

Use um repositório separado, **privado**, somente após revisar o conteúdo e a
privacidade do destino. Não inclua segredos, documentos completos desnecessários
de terceiros, config do Hermes ou bancos do GBrain. Repo privado também é cópia
externa. O backup nativo do Hermes não inclui este vault.

Exemplo após criar e conferir o repositório privado e autenticar com segurança:

```bash
cd /caminho/do/vault
git init -b main
# Selecione apenas arquivos revisados; confira git diff --cached antes do commit.
git add -- AGENTS.md
git commit -m "Inicia vault privado"
git remote add origin git@github.com:SEU_USUARIO/meu-vault-privado.git
git push -u origin main
```

Repita a seleção para os demais arquivos que decidiu incluir. Nunca aponte este
vault para o remoto público do template. Escolher backup no onboarding apenas
registra intenção: criação, cobertura e restauração precisam ser verificadas.
