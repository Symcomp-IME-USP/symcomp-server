#language: pt

Funcionalidade: Criar uma palestra
    Cenário: Organizador registra palestra com palestrante ainda não registrado
        Dado que Anna é organizadora
        Quando ela registra um novo palestrante corretamente
        E preenche as informações da palestra corretamente
        Então um email deve ser enviado a todos os palestrantes confirmando as informações

    Cenário: Organizador registra palestra com palestrante já registrado
        Dado que Anna é organizadora
        Quando ela preenche as informações corretamente
        Então um email deve ser enviado a todos os palestrantes confirmando as informações