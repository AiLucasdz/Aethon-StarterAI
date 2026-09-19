# Perfil de desempenho e limites

KVM 1 é ponto inicial para modelo remoto por API; não há benchmark de instalação
completa desta versão em VPS limpa. Nenhum LLM é instalado localmente.

- Conversas longas: `configurar_hermes.sh --perfil-leve` usa compactação nativa
  com threshold_tokens=300000 e tail_mode=lean, e max_turns=25. Valores iniciais
  ajustáveis, não garantia de tempo de resposta. Exigem Hermes compatível.
- Medir tokens por chamada, duração total do turno, número de ferramentas, RSS,
  erros e tempo de entrega. Cache reduz custo, mas não prova baixa latência.
- STT local small pode ser lento em 1 vCPU: não é ligado automaticamente. Escolher
  idioma/modelo/backend conforme necessidade e medir um áudio real autorizado.
- GBrain faz parte da instalação; Honcho e outros conectores exigem escolha. Não iniciar outra instância de PGLite
  para diagnóstico enquanto o gateway usa a base. Evitar descoberta/reindexação
  por mensagem e agendamentos simultâneos desnecessários.
- Não desativar memória para resolver lentidão sem evidência. Compactação mantém
  o histórico persistido, mas o resumo precisa preservar decisões e referências.
- Validação local de scripts não é teste de Telegram, OAuth ou modelo real.

O hook `aethon-memory` consulta uma vez por turno substantivo: sem LLM próprio,
recall limitado a 1.800 tokens estimados/6s e contexto total até 6.000 caracteres.
Confirmações breves, grupos e subagentes não consultam memória privada. Trechos
atuais são lidos sem cache local; GBrain pode usar seu cache nativo. Base nova
começa sem embeddings, sem síntese e sem enriquecimento periódico. Não confundir
isso com conversa gratuita: o modelo processa o contexto e seu replay.

Tudo criado prioriza desempenho, custo e manutenção. Evite código, instruções e
camadas redundantes; não sacrifique clareza ou validação para reduzir linhas.
