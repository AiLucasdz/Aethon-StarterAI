
# Atualizações — como funciona para quem fez fork

## O princípio: base atualizável + personalização preservada

Este repositório é uma **base**. A sua instalação tem três camadas:

| Camada | Onde vive | O que acontece na atualização |
|---|---|---|
| **Base** (código, docs, templates) | repositório público | atualiza do upstream |
| **Personalização** (soul, config) | seu servidor, fora do git público | **preservada sempre** |
| **Dados** (memórias, conversas, tokens) | seu servidor, fora do checkout | **nunca tocada** |

## Fluxo de atualização

```bash
# 1. backup antes de qualquer coisa (obrigatório)
tar czf ~/backup-hermes-$(date +%F).tar.gz ~/.hermes --exclude='.hermes/hermes-agent'

# 2. atualizar a base
cd ~/SEU_FORK
git pull upstream main

# 3. rodar o migrador (aplica mudanças de base, pula tudo que é seu)
./scripts/update.sh
```

## Garantias e limites honestos

- O `update.sh` só toca na camada **base**. Soul, config, memórias e dados
  do dono são intocados por design.
- **Se você modificar arquivos da base** (código), pode haver conflito —
  aí o migrador para e te mostra o diff para decidir. Não prometemos
  ausência de conflitos em forks que alteram código.
- Cada release lista migrações versionadas; reversão documentada por release.

## Releases

O upstream publica releases com:
- changelog legível (o que mudou e por quê)
- IDs de modelo recomendados **conferidos na data da release** (mudam rápido)
- instruções de migração quando necessário
