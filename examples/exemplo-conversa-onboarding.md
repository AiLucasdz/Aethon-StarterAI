# Exemplo de onboarding — dados fictícios

Cada pergunta ocorre em um turno. A implementação obtém o texto de `onboarding.py`.

**Agente:** Como você quer me chamar?

**Dona:** Aurora.

**Agente:** Como você quer ser chamada?

**Dona:** Pessoa Exemplo.

**Agente:** O que você faz?

**Dona:** Trabalho com design.

**Agente:** O que você mais quer que eu faça por você?

**Dona:** Ajudar a encontrar decisões e organizar projetos.

**Agente:** Tem algo que eu nunca devo fazer?

**Dona:** Enviar mensagens sem meu pedido.

**Agente:** Como prefere minhas respostas?

**Dona:** Curtas e diretas.

**Agente:** Em que fuso você está?

**Dona:** UTC.

**Agente:** Quer ajustar também o nome do bot no BotFather?

**Dona:** Pular.

**Agente:** Quer configurar backup privado depois? Não envie tokens aqui.

**Dona:** Pular.

**Agente:** GBrain faz parte do agente. Posso configurar também Honcho para
continuidade entre conversas? Ele processa contexto no serviço e pode ter custo.

**Dona:** Pular.

**Agente:** Identidade configurada; Honcho recusado e backup não configurado.
Vou concluir a instalação do GBrain e conferir a recuperação no seu perfil.
Agenda e outras conexões podem ser configuradas depois, quando você pedir.

O agente só anuncia recuperação funcionando após a verificação real. Se faltar
uma dependência ou recarga do runtime, informa a etapa pendente. Se Honcho fosse
aceito, iniciaria também seu setup seguro; nenhuma credencial entraria na conversa.
