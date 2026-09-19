# Atualizações de forks

## Pelo Telegram ou conversa com o agente

Ao concluir a instalação, o agente configura uma consulta **a cada sete dias** e
informa: “Vou conferir melhorias do template semanalmente e avisar aqui quando
houver atualização pendente. Para aplicar, diga: **verifique e atualize meu agente
pelo template**.” Não prometa lançamentos semanais.

A consulta usa script no cron nativo do Hermes, **sem LLM**, sem merge, sem migração
e sem alterar arquivos de trabalho. Sem novidade, não envia mensagem. Havendo
atualização ainda não aplicada, lembra no ciclo semanal. Falhas de rede ficam no
histórico local do cron; não viram mensagem falsa de que está atualizado.

- **“Tem atualização do template?”**: consultar o repositório original verificado,
  comparar a revisão instalada com a disponível e resumir mudanças/pendências,
  sem aplicar migração ou alterar o runtime.
- **“Verifique e atualize meu agente pelo template”**: executar o fluxo abaixo,
  revisar o changelog e aplicar somente mudanças compatíveis. Informar revisão
  anterior/nova, o que mudou e validações ou conflitos restantes.
- Se não houver novidade, informar “já está atualizado”; não reinstalar nem
  reabrir onboarding. Um fork divergente exige revisão antes de aplicar.

Atualizar o template não equivale a atualizar Hermes ou trocar modelo de conversa,
STT, provider, credenciais ou conexões personalizadas. Nunca copiar dados de outra
instalação para resolver conflito.

## Instalar a consulta semanal

Depois da preparação principal e antes de encerrar o onboarding, no mesmo perfil:

```bash
python3 scripts/ativar-atualizacoes.py --telegram-owner ID_CONFIRMADO_NO_DM
```

O agente resolve o ID pelo remetente da conversa privada, sem pedir token ou
usar ID de grupo. Pode indicar `--hermes CAMINHO` para o executável do perfil.
O script cria `aethon-atualizacoes-semanais`, intervalo de sete dias desde a
instalação, `--no-agent`, destino Telegram explícito e falhas somente locais.
Consulta somente o repositório oficial; não segue uma troca arbitrária de remote.

Reexecução preserva job existente, inclusive pausa e destino; não cria duplicata.
Se já houver job, verificar `hermes cron list --all`, script, destino e estado
antes de anunciar que está ativo. Usar comandos nativos para ajustes autorizados.
Se faltarem `--no-agent`, scheduler funcional ou Telegram, informar pendência;
não substituir por chamadas semanais ao modelo nem por um daemon novo.

Validar o script (`python3 scripts/verificar-atualizacoes.py`), cadastro e
`hermes cron status`. Saída vazia é normal quando não há novidade. Confirmar
entrega quando houver aviso real; job cadastrado não comprova entrega. Não
fabricar atualização nem enviar mensagem de teste para comprovar funcionamento.
Em instalação só por CLI, o aviso Telegram fica pendente até existir DM confirmado.

Para desativar, o dono pode dizer “pare os avisos de atualização”; o agente executa
`hermes cron pause ID_DO_JOB` e confirma o estado. Para retomar, usa `resume`.
Uma atualização do template não reativa uma pausa. Não instalar essa rotina em
instalações antigas por migração silenciosa; configurar quando o dono solicitar.

## Execução pelo agente

A base e os dados privados ficam em diretórios separados. Nunca coloque o vault,
HERMES_HOME ou backups dentro do checkout, mesmo que estejam no .gitignore.

Configure o remote `upstream` para o repositório original verificado. Execute
`bash scripts/update.sh upstream main`. O script exige checkout limpo, busca o
remote, recusa divergência e atualiza somente por fast-forward. Antes da alteração
cria e verifica um bundle privado do Git; falha de backup interrompe a atualização.
Um fork com commits próprios exige revisão e merge manual. Não usar force/reset
para contornar conflitos. O bundle e o hash anterior permitem recuperar o código
em outra pasta sem apagar suas mudanças.

Este processo não atualiza Hermes nem migra dados privados sozinho. Com o mesmo
HERMES_HOME e VAULT_PATH, rode `iniciar.py` para criar apenas fontes ausentes e
`migrar.py --apply` para atualizar a base gerenciada do SOUL. A migração guarda
backup, oferece `--rollback ID` e recusa alterações locais no bloco gerenciado.
Identidade, regras e dados fora do bloco são preservados. Onboarding concluído
anteriormente é reutilizado; a antiga escolha segundo_cerebro vira escolha Honcho.
GBrain passa a integrar a instalação, preservando configurações existentes.

Rode `ativar-memoria.py` com o dono/perfil correto para instalar o hook e GBrain.
Backups desse comando cobrem config.yaml, não o banco nem o vault externo.
Se o GBrain existente usa stdio, a ativação relata pendência sem sobrescrevê-lo:
execute a [migração exclusiva para HTTP local](gbrain-runtime.md) fora do turno
ativo. Não anunciar atualização funcional só porque o checkout avançou.
O symlink do plugin acompanha o checkout: atualizar o código exige recarga do
runtime fora de turnos ativos e nova validação. Em restore para outra máquina,
refaça essa ativação para corrigir caminhos; não reutilize diretórios do host antigo.
Leia o changelog e valide o consumidor antes de anunciar atualização concluída.
