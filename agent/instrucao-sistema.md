# Referência para outros agentes

O runtime Hermes recebe `base-operacional.md` pelo bloco gerenciado do SOUL;
não carrega este arquivo automaticamente. A identidade escolhida e os caminhos
privados são projetados por `scripts/migrar.py`, inclusive em SOUL preexistente.

O contrato de captura, revisão e aplicação está em [memoria.md](memoria.md).
Evite manter uma segunda versão dessas regras aqui. Para outro runtime, adapte
seu carregador de instruções e recuperação e valide o consumidor; copiar este
arquivo não instala o plugin Hermes.
