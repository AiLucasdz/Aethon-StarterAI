# Atualizações de forks

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
