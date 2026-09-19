# GBrain compartilhado no runtime

O PGLite aceita um único processo proprietário do banco. Branches e worktrees
separam código, mas **não** separam banco, configuração ou portas. Dois processos
`gbrain serve` sobre a mesma base causam falha, mesmo em checkouts diferentes.

## Instalação nova

`ativar-memoria.py` usa o servidor HTTP nativo, com sete verbos, autenticação e
bind somente em `127.0.0.1`. Um serviço systemd de usuário por perfil mantém o
banco aberto; gateway, CLI Hermes e cron conectam ao mesmo endpoint. Não executar
outro CLI GBrain que abra diretamente essa base enquanto o serviço estiver ativo.

O instalador requer Bun e systemd de usuário funcional. Sem supervisor, relata
pendência e não substitui a solução por stdio. Em VPS, verificar que o gerenciador
de usuário inicia no boot e permanece ativo sem sessão SSH (`loginctl show-user
"$(id -un)" -p Linger`); se necessário, o administrador habilita linger para esse
usuário. Não declarar disponibilidade após reboot sem verificar essa condição.

O recibo privado `<HERMES_HOME>/state/aethon-memory/gbrain-service.json` informa
nome da unidade, endpoint e caminho da base. Token fica no `.env` privado do perfil;
o config referencia a variável, sem segredo na linha de comando ou no Git.
A unidade reinicia após saída do processo, com intervalo de cinco segundos e
limite de cinco partidas por minuto. Reinício não corrige disco cheio, credencial
inválida ou configuração incorreta: conferir `systemctl --user status UNIDADE`
e `journalctl --user -u UNIDADE`. Não expor logs/credenciais no chat público.

Uma instalação parcial pode ser retomada pelo mesmo comando: o recibo evita
reimportar o banco servido. Falha posterior no plugin pode deixar esse serviço
preparado; retomar a instalação ou desabilitar a unidade identificada no recibo.
Para desinstalar, primeiro remover/reconfigurar o MCP nos consumidores; então
`systemctl --user disable --now UNIDADE`. Não apagar a base como procedimento de reparo.

A base nova continua sem embeddings/API e sem custo de modelo na inicialização.
Se habilitar embeddings ou síntese depois, fornecer ao serviço suas credenciais
por EnvironmentFile privado (600), além da configuração nativa do GBrain; não
presumir que o serviço herda o ambiente do gateway.

## Instalação existente e migração

HTTP existente é preservado; testar seu consumidor antes de anunciar pronto.
Servidor stdio existente é preservado, mas o instalador encerra com uma pendência
explícita: a migração precisa de uma janela exclusiva. Não interromper o turno
Telegram que está executando a instalação. Agendar a operação fora desse processo
ou executá-la pelo terminal, com recuperação preparada.

O agente responsável deve:

1. Identificar todos os consumidores, base real, serviço do gateway e configuração
   vigente. Preservar modelo, providers, credenciais, escopos e opções de memória.
2. Drenar/parar os consumidores e o proprietário atual. Fazer cópia consistente
   da base e das configurações em diretório privado. Nunca apagar lock de processo vivo.
3. Com a base fechada, criar token nativo `gbrain auth create NOME --scopes read,write`,
   capturando a saída somente em arquivo privado. Não reimportar nem criar outra base.
4. Instalar uma unidade equivalente à gerada em `scripts/gbrain_service.py`, usando
   o **GBRAIN_HOME existente**, porta local livre e EnvironmentFile privado com as
   credenciais necessárias. Iniciar e verificar saúde/autenticação.
5. Pelo mecanismo nativo do Hermes, substituir apenas o MCP GBrain por URL HTTP e
   header Bearer via variável privada. Reiniciar os consumidores. Se falhar, parar
   o HTTP antes de restaurar o transporte anterior; nunca abrir os dois juntos.
6. Testar dois clientes Hermes simultâneos, recall de informação existente com
   proveniência e reinício controlado. Verificar também o preflight das rotinas.
   Não fabricar fatos sobre o dono, reexecutar ingestões ou enviar mensagens de teste.

Configurar o destino de falha de cada rotina pelo cron nativo e validar a composição
do aviso sem fabricar incidentes reais. O Hermes pode deduplicar o mesmo bloqueio
até uma execução saudável: não prometer aviso a cada tentativa. O plugin informa
falha de memória no contexto do modelo, preserva fontes locais e registra warning;
isso não comprova que todo modelo sempre comunicará a limitação corretamente.

## Testes e promoção

Trabalhar em branch de correção; validar e revisar antes de publicar na oficial.
Cada teste de runtime precisa de HERMES_HOME, vault, GBRAIN_HOME e porta próprios.
`scripts/testar-runtime.py --gbrain ...` cria esse ambiente, testa escrita/releitura
fictícia e clientes concorrentes, e desativa/remove a unidade de teste ao terminar.
Nenhuma credencial pessoal ou dado de produção deve entrar na fixture.
