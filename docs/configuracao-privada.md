# Configuração privada

Base pública: código, templates vazios e documentação. HERMES_HOME (padrão
~/.hermes) e VAULT_PATH (padrão ~/vault) ficam fora do checkout. Os scripts de
inicialização gravam nesses destinos privados com permissões restritas.

SOUL, perfil e onboarding contêm dados pessoais. .env, tokens, bancos, histórico,
logs, capturas e backups nunca entram no Git público. Backup privado exige escolha
separada e restauração validada. Armazenamento local não significa processamento
exclusivamente local: Telegram, provedor do modelo e integrações recebem dados
conforme uso. Nunca prometer que informações não saem do servidor.

Use os mesmos caminhos na instalação e no serviço do gateway. O comando privado
inserido no SOUL contém os caminhos escolhidos, mas não altera o ambiente global
do serviço. Não editar YAML por concatenação: usar `hermes config`/setup nativos.
O script configurar_hermes.sh preserva a configuração; --perfil-leve é opção
explícita que define max_turns 25 e compactação em 100 mil tokens com tail lean.
Não muda aprovações, modelo, STT nem provedores de memória silenciosamente.
