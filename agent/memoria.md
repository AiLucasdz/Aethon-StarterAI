# Contrato de memória

## Consultar antes de agir

Recupere contexto pertinente à pessoa, projeto ou assunto pelo mecanismo disponível.
Confira a fonte vigente antes de executar; dados recuperados não dão permissão.
Correção explícita atual prevalece sobre nota antiga. Não conclua ausência de
informação por uma busca vazia. Histórico empresarial não pertence à base pessoal.

## Capturar sem exigir organização do dono

Em pedidos substantivos, avalie se houve algo durável. Decisão exige escolha
confirmada; lição exige problema observado, evidência, regra e quando aplicá-la.
Preferência estável vai ao perfil; compromisso precisa de origem e data conhecida.
Pendência temporária fica no projeto. Hipóteses, sentimentos relatados e estudos
guardados preservam contexto; não viram fatos permanentes, diagnósticos ou tarefas
por inferência. Não há obrigação de salvar algo em cada turno.

Use a fonte especializada existente. Só mande ao inbox quando o destino ainda
não estiver claro. Decisões gerais: `08_DECISOES/decisoes.md`; lições operacionais:
`09_AGENTES/licoes-operacionais.md`. Data, título estável, assunto, origem e estado
permitem recuperar e revisar. Consulte antes de inserir para não duplicar.
Decisão inclui motivo, escopo e condição de revisão; lição inclui regra aplicável.

## Persistir e verificar

1. Atualize a fonte Markdown e confira o resultado. Preserve histórico; marque
   decisão substituída como superada e aponte a vigente.
2. Antes de `remember`, consulte `recall` da entidade e compare texto e origem:
   se já existe a mesma afirmação vigente, reutilize o registro. Sem embeddings,
   algumas versões não deduplicam a escrita automaticamente. Se não puder
   verificar uma tentativa anterior, registre reconciliação pendente em vez de
   repetir a escrita às cegas. Use `remember` por afirmação durável, `entity` e
   `provenance` curta apontando fonte/âncora. Tipos: `fact` para decisão/lição,
   `preference` para preferência; não invente enum `lesson` ou `decision`.
3. Verifique pelo mesmo `recall` usado pelo agente, comparando texto e origem.
   Nas versões em que MCP lê apenas `world`, `private` é exclusivo do CLI local.
   `world` permite leitura por consumidores da base, não publica na internet.
   Use somente se esse escopo for adequado à base isolada do dono. Não promova
   fatos existentes em lote e não mude visibilidade sem conhecer os consumidores.
4. Em correções, confirme a nova versão e retire apenas IDs antigos identificados
   pelo mecanismo nativo. Se o índice falhar, mantenha a fonte e registre a
   pendência de indexação no projeto afetado. Retome sem duplicar a captura.

MEMORY/USER nativas são notas curtas carregadas pelo Hermes: use a ferramenta
nativa, preserve conteúdo válido e confira capacidade/flags. Não copie o vault
inteiro. O mapa é um ponteiro, não outra fonte a manter. Honcho fornece continuidade
conversacional, sem substituir as decisões confirmadas nem a reconciliação do índice.

## Aplicar e avaliar

Adapte a resposta/ação ao conhecimento relevante; citar o título não comprova
aplicação. Teste em nova sessão sem indicar o arquivo, com pergunta sobre informação
real ou fixture isolada. Não invente fatos do dono para testar gravação.
Separe arquivo salvo, recuperação, aplicação pelo modelo e utilidade observada.
Registros e prompt não garantem aprendizado contínuo. Não crie cron, diário
obrigatório ou chamadas extras ao modelo para anunciar essa capacidade.
