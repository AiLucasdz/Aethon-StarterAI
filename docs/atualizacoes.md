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

Este processo NÃO faz backup consistente do runtime, NÃO atualiza o Hermes e NÃO
migra dados privados. Migrações versionadas de configuração e atualização da base
operacional do SOUL ainda não estão implementadas. O onboarding preserva o SOUL
existente; uma correção no template não muda automaticamente instalações antigas.
Leia o changelog antes de atualizar. Não anunciar atualização completa da instalação
até existirem migrações testadas e recuperação de dados validada.
