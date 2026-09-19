# Instalação pelo agente já conectado ao Telegram

O dono envia o link deste repositório ao seu Hermes e pede a instalação. Não é
necessário criar outro bot, trocar o modelo ou refazer o pareamento existente.
O vídeo de VPS, instalação do Hermes e conexão ao Telegram será incluído depois.

## Instruções ao agente instalador

1. Inspecione o repositório solicitado e suas instruções. Um link isolado não é
   autorização inequívoca para instalar: nesse caso pergunte se a pessoa quer
   a instalação. Se ela já pediu, prossiga sem repetir a confirmação.
2. Clone a base num diretório próprio, separado do runtime, vault e backups.
   Preserve checkout existente e alterações locais. Não copie dados de outra
   instalação e não envie credenciais ou arquivos privados ao Git público.
3. Identifique o `HERMES_HOME` do processo/perfil que atende esta conversa e o
   `VAULT_PATH` escolhido (ou um diretório privado fora do checkout). Não assuma
   o perfil padrão quando houver vários. Se não conseguir identificar o runtime,
   esclareça antes de alterar arquivos. Não imprima variáveis com segredos.
4. Execute `python3 scripts/iniciar.py` no checkout com esses dois caminhos no
   ambiente. O comando cria apenas arquivos ausentes, prepara o onboarding e
   instala a base gerenciada com backup local dos arquivos migrados. Não instala
   serviços, não conecta contas e não altera a configuração do Hermes.
5. Confira o código de saída e execute `python3 scripts/migrar.py --status` com
   o mesmo ambiente. Em caso de erro, informe a causa e corrija antes de anunciar
   instalação concluída. Não remova personalizações para contornar conflitos.
6. Execute `python3 scripts/gateway_hook.py` e apresente a pergunta retornada
   nesta conversa. Primeiro nome do agente, depois nome do dono. Para responder,
   use `--responder CHAVE RESPOSTA` com argumentos separados/escapados; para pular,
   `--pular CHAVE`. Não interpole o texto do usuário em comandos shell.
7. Ajude com outros pedidos durante o onboarding. Todas as perguntas podem ser
   puladas. O estado em disco permite retomar depois; novas sessões carregam o
   SOUL atualizado. Não reinicie o gateway no meio da conversa só para atualizar
   instruções; nesta sessão siga o fluxo lido no repositório.
8. Ao concluir, ofereça uso imediato ou configuração opcional. Agenda, Tasks e
   YouTube são exemplos independentes. Novas automações também podem ser pedidas.
   Registre a escolha com `scripts/modulos.py`; isso registra intenção, sem
   conectar contas ou agendar tarefas. Implemente e teste cada escolha antes de
   declarar funcionamento. Não bloqueie o uso esperando integrações opcionais.

## Atualizações solicitadas pelo dono

Leia o changelog e `docs/atualizacoes.md`. Atualize a base e aplique a migração
privada no runtime identificado. A base gerenciada do SOUL recebe melhorias;
identidade e texto fora do bloco são preservados. Mudança local dentro do bloco
gera conflito explícito. Não sobrescreva config do Hermes nem ative novos módulos.

## Limite da validação

Os testes isolados exercitam instalação, retomada, escolhas, atualização e
reversão com dados fictícios. Eles não comprovam obediência do modelo nem entrega
real pelo Telegram. Esse teste exige bot separado pareado com o responsável;
nunca use o bot de produção para simular uma instalação vazia.
