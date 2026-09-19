# Conectores opcionais

Nenhum conector externo é ligado por padrão. `scripts/modulos.py` registra
intenção; não instala adaptadores. GBrain e Honcho seguem o fluxo separado de
[memória](segundo-cerebro.md).

## Configurar e verificar

1. Partir do pedido do dono e registrar o escopo. Esclarecer apenas o que faltar;
   não repetir confirmação para a ação já autorizada.
2. Descobrir skills/MCPs disponíveis na versão instalada do Hermes e ler suas
   instruções atuais. A existência de um exemplo abaixo não garante que a skill
   ou entrada de catálogo esteja instalada.
3. Explicar custos e permissões pertinentes. Autenticar no fluxo seguro do serviço,
   com conta do próprio dono. Usar callback OAuth/device flow quando disponível;
   segredos e códigos de troca somente em entrada protegida, nunca no chat, Git
   ou argumentos de comandos. Não reaproveitar conta de outra instalação.
4. Consultar o serviço pelo consumidor que o agente usará. Resposta vazia válida
   pode comprovar acesso; erro de autenticação/permissão ou resposta simulada não.
5. Registrar o estado observado, a evidência sem segredos e as pendências.
6. Ativar rotinas apenas quando pedidas, com frequência/destino definidos e teste
   de execução e entrega. Conectar uma conta não autoriza uma rotina.

## Exemplos de escopo

| Serviço | Configuração e prova necessária |
|---|---|
| Google Agenda / Tasks / Gmail | OAuth do dono com escopos necessários; consultar cada serviço solicitado |
| YouTube público | Ferramenta de leitura/transcrição disponível; testar URL permitida. Privado/não listado exige cuidado com destino do conteúdo |
| Canal YouTube do dono | OAuth e escopos próprios; consulta real de canal/métricas. Não vem implementado como adaptador neste template |
| Fathom / reuniões | Integração oficial ou MCP disponível e autenticação própria; listar recurso autorizado |
| X e outras redes | Ferramenta/API disponível, custos/permissões conferidos; publicação somente sob autorização específica |

Esta lista não limita novas conexões. Se não houver adaptador compatível,
implemente e teste ou registre a lacuna; nunca anuncie funcionamento por ter
somente salvo credenciais ou marcado intenção. Não use o bot de produção de
outra pessoa para testar uma instalação nova.
