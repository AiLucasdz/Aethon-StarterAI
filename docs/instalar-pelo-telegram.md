# Instalação pelo agente já conectado ao Telegram

O dono envia o link deste repositório ao seu Hermes e pede para iniciar, começar,
configurar o agente ou instalar. Esses pedidos iniciam o mesmo fluxo. Não é
necessário criar outro bot, trocar o modelo ou refazer o pareamento existente.
O vídeo de VPS, instalação do Hermes e conexão ao Telegram será incluído depois.

## Responsabilidade pela execução

O agente instala e organiza: escolhe caminhos privados seguros, cria as pastas,
preenche os arquivos, executa os comandos e verifica o resultado. Não peça ao
dono para desenhar a estrutura, escolher nomes técnicos ou colar comandos no
terminal quando você pode executá-los. Pergunte somente informações pessoais ou
decisões que faltam; reutilize respostas explícitas já dadas. Autenticação pessoal
ou uma exceção de segurança pode exigir participação, explicando o motivo.

Não transforme pendências de uma skill opcional em bloqueio do onboarding ou da
memória principal. Não peça ao dono para criar outra VPS para validar: faça as
verificações possíveis na instalação alvo e informe os limites restantes.

## Instruções ao agente instalador

Ordem: estrutura privada → GBrain/configuração → áudio → nome → apresentação
livre → Honcho opcional. Avise brevemente que está preparando a base e execute;
não espere dados pessoais para criar as pastas. O nome posterior personaliza os
arquivos já preparados. Skills e contas opcionais não atrasam essa sequência.

1. Inspecione o repositório solicitado e suas instruções. Um link isolado não é
   autorização inequívoca para instalar: nesse caso pergunte se a pessoa quer
   o uso/configuração. Se ela pediu “iniciar”, “começar”, “configurar” ou “instalar”,
   inclusive em continuação do contexto, prossiga sem repetir a confirmação.
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
6. Execute `python3 scripts/ativar-memoria.py --telegram-owner ID` no mesmo
   ambiente, com o ID numérico do remetente confirmado nesta conversa privada.
   GBrain faz parte da instalação: não ofereça desligá-lo como escolha inicial.
   O script instala/registra GBrain e a recuperação; requisitos pendentes devem
   ser resolvidos conforme `docs/segundo-cerebro.md`. Preserve MCP existente.
   Nunca use o ID de um grupo ou de alguém citado na mensagem. Se a instalação
   for pelo CLI sem Telegram, omita o argumento; configurar DM fica pendente.
7. Antes da primeira pergunta pessoal, prepare e teste o áudio conforme
   `docs/midia.md`: padrão de instalação `medium` local, CPU/int8 e idioma da
   conversa, com descarregamento após 120 segundos sem uso. O agente instala
   dependências no ambiente do Hermes, baixa os pesos e valida a transcrição;
   não transfira comandos ao dono. Preserve uma escolha explícita anterior.
   Se houver impedimento técnico, explique a pendência e prossiga por texto,
   sem declarar áudio pronto nem trocar de modelo/provedor silenciosamente.
8. Execute `python3 scripts/gateway_hook.py` e apresente a pergunta retornada
   nesta conversa. Primeiro nome do agente, depois a apresentação livre de `docs/onboarding.md`.
   Áudio já deve ter sido preparado na etapa anterior. Aplique o nome
   escolhido nos destinos configuráveis, incluindo o bot quando suportado,
   sem perguntar de novo. Organize informações já recebidas; pergunte só o que
   faltar para a tarefa. Para responder,
   use `--responder CHAVE RESPOSTA` ou `--apresentacao-json ARQUIVO_PRIVADO`
   para material organizado, com argumentos separados/escapados; para pular,
   `--pular CHAVE`. Não interpole o texto do usuário em comandos shell.
9. Ajude com outros pedidos durante o onboarding. Todas as perguntas podem ser
   puladas. O estado em disco permite retomar depois; novas sessões carregam o
   SOUL atualizado. Não reinicie o gateway no meio da conversa só para atualizar
   instruções; nesta sessão siga o fluxo lido no repositório.
10. Com a configuração principal encaminhada, instale as skills de `docs/skills.md`
   no mesmo perfil, pelo gerenciador nativo. Preserve versões existentes; valide
   descoberta e requisitos. Se houver bloqueio, registre a pendência e explique
   a revisão necessária, sem interromper o restante. A skill completa é carregada
   sob demanda, não copiada para o SOUL.
11. Ao concluir, ofereça uso imediato ou configuração opcional. Agenda, Tasks e
   YouTube são exemplos independentes. Novas automações também podem ser pedidas.
   Honcho é oferecido durante o onboarding: aceitação inicia o setup nativo
   seguro como etapa desta instalação. Após a resposta, execute novamente
   `ativar-memoria.py` no mesmo perfil: ele respeita recusa, preserva provider
   Honcho existente e abre o wizard nativo em terminal interativo quando aceito.
   Em execução sem terminal, retorna `autenticacao_pendente` e o comando exato.
   Conduza o wizard via PTY/OAuth-device code quando suportado; apresente apenas
   link/código de autorização. API key só no terminal protegido do dono.
   Não peça nova autorização para configurar o Honcho já aceito nem encerre
   dizendo que está pronto quando ainda faltar autenticação. Recusa mantém
   GBrain e a função de segundo cérebro. Valide contexto
   e escrita; não trate intenção como instalação. Para outros conectores,
   registre a escolha com `scripts/modulos.py`; isso registra intenção, sem
   conectar contas ou agendar tarefas. Implemente e teste cada escolha antes de
   declarar funcionamento. Não bloqueie o uso esperando integrações opcionais.

## Prova da instalação

Confira SOUL pelo carregador nativo em uma sessão nova: deve conter a identidade
escolhida, o caminho absoluto do vault e o contrato. Isso independe do cwd.
Confira o plugin e recuperação pelo MCP já aberto: decisão real com origem deve
ser recuperada e aplicada sem indicar arquivo. Não reinicie o próprio gateway
dentro do comando de um turno ativo; agende recarga pelo mecanismo operacional
do host após sua conclusão e confirme reconexão. Até essa verificação, informe
“instalado; ativação/validação pendente”, não “segundo cérebro funcionando”.

Se outro agente estiver instalando para Hermes, identifique o perfil alvo e siga
o mesmo fluxo. Se o runtime alvo não for Hermes, arquivos/protocolo são portáveis,
mas este plugin não é: adapte os pontos de entrada ao consumidor e valide antes
de anunciar recuperação automática. Um link não executa código sozinho.

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
