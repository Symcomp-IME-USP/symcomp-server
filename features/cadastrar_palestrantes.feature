#language: pt

Funcionalidade: Cadastrar um novo palestrante
    Cenário: Organizador cadastra palestrante que não é usuário
        Dado que Anna é organizadora
        Quando ela insere corretamente as informações sobre o palestrante
        Então deve ser enviado um email com o código de primeiro acesso do palestrante
        E ele deve poder ver o cronograma, mas não pode obter detalhes sobre as outras palestras

    Cenário: Organizador cadastra palestrante que já é usuário
        Dado que Anna é organizadora
        Quando ela insere corretamente as informações sobre o palestrante
        Então o palestrante não deve receber código de primeiro acesso por email
        E ele deve poder ver o cronograma, mas não pode obter detalhes sobre as outras palestras