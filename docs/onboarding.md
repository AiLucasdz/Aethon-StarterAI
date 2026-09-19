# Configuração inicial pelo Telegram

Pré-requisitos: Hermes instalado, modelo configurado e bot pareado com o dono.
A instalação é apresentada em vídeo pelo mantenedor (link ainda pendente).
O dono pode enviar este repositório ao agente já conectado e pedir a instalação;
o agente segue `instalar-pelo-telegram.md`. Não é necessário pedir ao dono que
execute scripts manualmente. Para instalação manual, execute
`bash scripts/iniciar.sh` no terminal com HERMES_HOME e VAULT_PATH corretos.
O inicializador prepara os templates e adiciona ao SOUL uma instrução para chamar
`gateway_hook.py`. É uma instrução ao modelo, não um callback nativo garantido.
A próxima sessão precisa carregar esse SOUL; uma simulação local não comprova
que o Telegram real cumpriu o fluxo.

Primeiro o nome do agente, depois nome do dono, necessidades, limites, estilo e
fuso. Todas as perguntas aceitam pular; o estado permite retomar depois.
Ajude em pedidos úteis durante a configuração; não obrigue completar o questionário.
Use a pergunta atual, sem enviar respostas fora de ordem. O fuso precisa ser IANA.
A escolha de nome orienta /setname no BotFather; não troca o username automaticamente.

O passo opcional de GitHub registra apenas interesse em backup. NUNCA pedir PAT,
senha ou chave no chat. Autenticação deve ocorrer no terminal por fluxo nativo
seguro. O template não cria, verifica ou sincroniza repositórios privados nesta
versão e não anuncia backup como concluído. Token antigo salvo na instalação não
é apagado automaticamente; nunca copiar para o projeto público.

Depois, a pessoa escolhe conexões e, separadamente, rotinas. Módulos ainda sem
adaptador não podem ser anunciados como ativos. Ver catalogo-modulos.md.
