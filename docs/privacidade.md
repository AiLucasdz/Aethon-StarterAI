# Privacidade

Nunca colocar dados de instalação no checkout público. Revisar arquivos,
metadados Git, histórico, tags, releases, artefatos e logs antes de publicar.
.gitignore e busca de padrões ajudam, mas não provam ausência de dados pessoais.
Um histórico reescrito não remove cópias, forks ou caches de terceiros; em caso
de credencial exposta, revogar e substituir a credencial é necessário.

Arquivos privados permanecem no servidor por padrão. Conteúdo do SOUL, memórias,
notas recuperadas e conversa pode entrar no contexto enviado ao modelo via
OpenRouter. Mensagens passam pelo Telegram. Honcho, embeddings e outras conexões
podem receber dados quando configurados. Não confundir localização do arquivo
com local de processamento. Backup remoto privado também é uma cópia externa.

Tokens: somente pelo fluxo seguro do serviço no terminal/OAuth; nunca no chat,
argumentos de comandos ou Git. O onboarding registra intenção de backup, não
coleta token nem configura armazenamento global de credenciais.

Releases devem passar por revisão humana e varredura de padrões, incluindo
identificadores conhecidos mantidos em lista PRIVADA, nunca embutidos no scanner
público. Não publicar achados que reproduzam os dados removidos.
