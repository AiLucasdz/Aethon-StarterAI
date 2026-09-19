
# Contrato de configuração privada

> Define onde cada coisa viva na instalação do dono. A base pública nunca
> grava nada aqui; o agente e os scripts leem, nunca escrevem para fora.

## Locais (padrão da instalação)

| Camada | Caminho no servidor | Versionado? |
|---|---|---|
| Motor (runtime Hermes) | `~/.hermes/hermes-agent/` | não — instalado por mecanismo oficial |
| **Soul do agente** | `~/.hermes/SOUL.md` | **nunca** (dados do dono) |
| Config local (modelo, tokens, fuso) | `~/.hermes/config.yaml` + `.env` | **nunca** |
| Credencial GitHub (backup do vault) | `~/.git-credentials` (perm. 600) | **nunca** |
| Memórias e notas do dono | pasta de vault do dono | escolha do dono (repositório privado dele) |
| Estado, logs, backups | `~/.hermes/state/`, logs do systemd | **nunca** |

## Regras do contrato

1. **A base pública não sabe nada sobre o dono.** Todo dado pessoal mora nos
   caminhos acima, fora do checkout.
2. **Atualização da base só toca o checkout público.** Os caminhos acima são
   intocados por design (ver `atualizacoes.md`).
3. **Placeholders `{{...}}`** nos templates são preenchidos uma única vez,
   pelo onboarding, e gravados nos caminhos privados.
4. **Credenciais**: `.env` local com permissão `600`. Nunca em chat, nunca em
   arquivo versionado.
5. O dono pode versionar SEU vault num repositório PRIVADO próprio; a base
   pública não estabelece nem exige isso.

## O que um fork pode mudar

- Caminhos privados: defina variáveis de ambiente uma vez (ex.: `HERMES_HOME`)
  e o resto da base lê delas — nunca caminhos absolutos fixados no código.
- Módulos: ativar/desativar por config; desligado = código não executa.
