#language: pt

Funcionalidade: Cadastrar um novo palestrante
    Cenário: Organizador cadastra palestrante que não é usuário
        Dado que Anna é organizadora
        Quando ela insere corretamente as informações sobre o palestrante
        Então deve ser enviado um email com o código de primeiro acesso do palestrante

    Cenário: Organizador cadastra palestrante que já é usuário
        Dado que Anna é organizadora
        E o palestrante já é usuário
        Quando ela insere corretamente as informações sobre o palestrante
        Então o palestrante não deve receber código de primeiro acesso por email