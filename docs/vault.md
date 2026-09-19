
# Vault (memória em Markdown) — Obsidian é opcional

> O vault do agente é **só uma pasta de arquivos Markdown** no seu servidor.
> O Obsidian é um **leitor/editor opcional** para você navegar essa pasta
> visualmente. O agente funciona 100% sem Obsidian.

## Por que Markdown

- Formato aberto, legível por humanos e por agentes
- Versionável com git (histórico de tudo)
- Sem lock-in: troca de ferramenta sem converter nada

## Estrutura padrão do vault

A base traz um esqueleto vazio com a mesma organização do projeto original,
simplificada para uso geral:

```
meu-vault/
├── AGENTS.md              # regras do repositório para o agente
├── 00_INBOX/              # capturas brutas (áudio, ideias, links)
├── 01_IDENTIDADE/         # quem é o dono, princípios de decisão
├── 02_SAUDE_E_CORPO/      # saúde do dono (métricas só se ele informar)
├── 03_CARREIRA_E_NEGOCIOS/# carreira e negócios
├── 04_FINANCAS/           # finanças
├── 05_TAREFAS/            # tarefas (espelho do Tasks, se ativado)
├── 06_IA_E_AUTOMACOES/    # IA, agentes, automações e acervo de estudo
├── 07_DIARIO/             # diário diário (capturas, check-ins)
├── 08_DECISOES/           # decisões importantes com data e origem
├── 09_AGENTES/            # configuração e planos dos agentes
├── 10_PESSOAS_E_RELACOES/ # pessoas e relações (consentimento do dono)
└── 90_EXPORTS/            # resumos portáteis para novas IAs
```

## Como o agente usa

1. **Captura**: o dono manda qualquer coisa crua → agente salva em
   `00_INBOX/` e registra na memória de recuperação
2. **Consolidação**: periodicamente, o agente move o que virou conhecimento
   para a pasta certa, mantendo origem e data
3. **Recuperação**: "o que decidi sobre X?" → o agente busca no vault primeiro,
   índice vetorial ajuda a achar

## Regras que o template impõe (no AGENTS.md do vault)

- Os arquivos vencem qualquer memória interna do agente
- Uma fonte de verdade por assunto (nada duplicado)
- Nada sensível no vault se ele for versionado num repositório privado

## Versionando seu vault (opcional, recomendado)

O dono PODE criar um repositório **privado** só dele para o vault:

```bash
cd ~/meu-vault
git init && git add -A && git commit -m "início do meu vault"
git remote add origin git@github.com:SEU_USUARIO/meu-vault-privado.git
git push -u origin private-main
```

⚠️ Revisão de privacidade do dono antes do primeiro push — o vault contém
dados pessoais por definição. Nunca use o repositório público do template
para isso.

## Obsidian (opcional)

```bash
# no seu computador (não na VPS): aponte o Obsidian para uma cópia do vault
# via SSHFS/Syncthing, ou edite direto com "Obsidian Git" plugin
```

Sem Obsidian, qualquer editor + `ssh` já funciona. O agente lê os arquivos
direto no servidor.
