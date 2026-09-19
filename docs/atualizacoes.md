# Atualizações de forks

## Pelo Telegram ou conversa com o agente

Ao concluir a instalação, o agente informa: “O template pode receber melhorias.
Uma vez por semana, você pode pedir: **verifique e atualize meu agente pelo template**.
Eu confiro as mudanças, preservo suas personalizações e valido o resultado.”

Não é promessa de lançamento semanal. Não há timer de consulta instalado por
esse aviso. O dono não precisa operar Git nem reinstalar o agente.

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
O symlink do plugin acompanha o checkout: atualizar o código exige recarga do
runtime fora de turnos ativos e nova validação. Em restore para outra máquina,
refaça essa ativação para corrigir caminhos; não reutilize diretórios do host antigo.
Leia o changelog e valide o consumidor antes de anunciar atualização concluída.
