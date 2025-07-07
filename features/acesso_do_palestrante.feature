#language: pt

Funcionalidade: Palestrante faz acesso à plataforma
    Cenário: Palestrante recebe código de acesso
        Dado que a Kely recebeu o código de acesso por email
        Quando ela fornece o email e o código
        Então ela deve poder redefinir sua senha
        E fazer login com sua nova senha

    Cenário: Palestrante já era usuário
        Dado que a Kely já estava cadastrada como usuário
        Quando ela faz login
        Ela deve poder listar o cronograma e ver somente detalhes de sua palestra