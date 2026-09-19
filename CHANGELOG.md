# Alterações em revisão após v0.2.1

- Onboarding deixa de solicitar tokens pelo Telegram e não anuncia backup sem
  sincronização/restauração implementadas. GitHub opcional registra intenção.
- Perguntas respeitam ordem, fuso é validado, pular funciona pelo wrapper;
  estado é gravado atomicamente com lock e acesso restrito.
- Inicialização preserva arquivos existentes mesmo em vault parcial, recusa
  caminhos dentro da base pública e prepara instrução no SOUL carregável.
- Configuração Hermes usa comandos nativos; não concatena YAML nem muda
  automaticamente modelo, aprovações ou STT. --yolo é escolha explícita.
- Perfil leve opt-in usa max_turns=25 e compactação nativa em 100 mil tokens
  com tail lean. Necessita benchmark em VPS limpa e versão compatível do Hermes.
- Atualização realiza fetch/fast-forward, verifica backup Git, recusa alterações
  locais/divergência. Migrações de runtime/personalização seguem pendentes.
- Capturas usam ID exato por hash, lock e escrita atômica; data inválida recusada.
- Documentação distingue mecanismos existentes, integrações planejadas e testes
  locais. Memória, SOUL e histórico enviados ao modelo não são somente locais.

Validação: testes unittest isolados e análise sintática. Sem teste real de bot,
OAuth, instalação completa em VPS ou migração entre releases nesta revisão.
