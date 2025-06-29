#language: pt

Funcionalidade: Cadastrar usuário

    Cenário: Novo usuário faz cadastro com sucesso
        Dado que João está acessando pela primeira vez
        Quando ele preenhce as informações solicitadas
        Então ele deve estar logado na plataforma

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