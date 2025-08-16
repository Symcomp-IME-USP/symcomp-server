#language: pt

Funcionalidade: usuário gera certificado
    Cenário: Um ouvinte que não está logado gera o certificado
        Dado que a palestra está disponível para gerar certificado
        Quando a Larissa insere seu email, senha e o código de validação válido
        Então ela deve receber um email com o seu certificado

    Cenário: Um ouvinte que não está logado quer gerar o certificado com o código de validação incorreto
        Dado que a palestra está disponível para gerar certificado
        Quando a Larissa insere seu email, senha e um código de validação inválido
        Então ela não deve receber um email com o seu certificado

    Cenário: Um ouvinte tenta gerar certificado de uma outra palestra que não está disponível
        Dado que Larissa não está logada
        E a palestra não está disponível para gerar certificado
        Quando a Larissa insere seu email, senha e o código de validação válido
        Então ela não deve