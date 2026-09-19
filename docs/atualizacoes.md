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

O update.sh não atualiza o Hermes nem modifica o runtime. Depois de revisar o
changelog e atualizar o código, execute `python3 scripts/migrar.py --apply` com
HERMES_HOME apontando para a instalação correta. Novas instalações já executam
essa etapa pelo inicializador.

A migração versionada atualiza apenas o bloco `aethon-base` do SOUL e os arquivos
`state/modulos.json` e `state/aethon-version.json`. Identidade, texto fora do bloco,
escolhas de módulos e configuração do Hermes são preservados. Se alguém alterou
o bloco gerenciado localmente, o comando recusa a substituição e exige revisão.
Reexecutar sem mudanças é idempotente. Nenhuma conexão/rotina é ativada.

Antes de escrever, um backup privado dos arquivos afetados é gravado e relido em
`HERMES_HOME/state/aethon-migrations/`, com permissão 600. A saída informa o ID;
para reverter, use `python3 scripts/migrar.py --rollback ID` no mesmo ambiente.
A reversão recusa sobrescrever mudanças posteriores nos arquivos envolvidos.
Uma interrupção deixa transação pendente; reverta-a antes de reaplicar. Erros
durante a escrita tentam restaurar o conteúdo anterior automaticamente.

Esses backups contêm dados privados. São cópias locais apenas dos arquivos
migrados, não um backup completo do vault/runtime, nem backup externo. Não os
publique. Restauração integral em outra VPS e validação real do Telegram seguem
pendentes. `--status` informa a versão da base privada; o perfil opcional de
desempenho não é aplicado pelas migrações.
