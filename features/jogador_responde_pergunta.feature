#language: pt

Funcionalidade: Jogador responde pergunta
    Cenário: Jogador responde corretamente a uma pergunta
        Dado que existe um jogador
        * que existe um desafio
        E que existe perguntas no desafio
        Quando ele responde a uma pergunta
        E ela está correta
        Então ele deve receber pontos pelo acerto

    Cenaŕio: Jogador responde pergunta, mas está incorreta
        Dado que existe um jogador
        * que existe um desafio
        E que existe perguntas no desafio
        Quando ele responde a uma pergunta
        E ela está errada
        Então ele não deve receber pontos pela resposta