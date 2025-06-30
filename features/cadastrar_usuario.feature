#language: pt

Funcionalidade: Cadastrar usuário

    Cenário: Usuário preenche cadastro e recebe código de validação
        Dado que João está acessando pela primeira vez
        Quando ele preenche corretamente as informações solicitadas para cadastro
        Então ele deve receber um e-mail contendo um código de validação

    Cenário: Usuário valida código e efetiva login
        Dado que João recebeu o código de validação por e-mail
        Quando ele informa corretamente o código recebido
        Então ele deve estar logado na plataforma

    Cenário: Usuário solicita reenvio de código após não receber o primeiro
        Dado que João não recebeu o código de validação inicial
        E já se passou pelo menos 1 minuto desde o pedido anterior
        Quando ele solicita o reenvio do código de validação
        Então ele deve receber um novo e-mail com o código de validação

    Cenário: Usuário altera e-mail para receber código após não receber o reenvio
        Dado que João não recebeu o código de validação após solicitar reenvio
        E já se passou pelo menos 1 minuto desde o último pedido
        Quando ele altera o e-mail para um endereço válido diferente
        Então ele deve receber um e-mail com o código de validação no novo endereço

    Cenário: Usuário faz cadastro, mas já está cadastrado
        Dado que João já fez seu cadastro
        Quando ele tenta se cadastrar novamente
        Então ele deve ser avisado que já está cadastrado

    Cenário: Senha sem letras
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha sem letras
        Então ele deve ser avisado que a senha é fraca

    Cenário: Senha sem letras minúsculas
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha sem letras minúsculas
        Então ele deve ser avisado que a senha é fraca

    Cenário: Senha sem letras maiúsculas
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha sem letras maiúsculas
        Então ele deve ser avisado que a senha é fraca

    Cenário: Senha sem números
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha sem números
        Então ele deve ser avisado que a senha é fraca

    Cenário: Senha sem caracteres especiais
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha sem caracteres especiais
        Então ele deve ser avisado que a senha é fraca

    Cenário: Senha com menos de 8 caracteres
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha com menos de 8 caracteres
        Então ele deve ser avisado que a senha é fraca

    Cenário: Senha com mais de 255 caracteres
        Dado que João preencheu todas as informações solicitadas corretamente
        Quando ele tenta cadastrar uma senha com mais de 255 caracteres
        Então ele deve ser avisado que a senha é valida

    Cenário: Usuário faz cadastro pelo Google Auth (OAuth)
        Dado que João está acessando pela primeira vez 
        Quando ele clica em logar com Google
        Então ele deve estar logado na plataforma

    Cenário: Usuário faz cadastro pelo Google Auth (OAuth), mas já está cadastrado
        Dado que João já se cadastrou no sistema
        Quando ele clica em cadastrar com o Google
        Então ele deve estar logado na plataforma