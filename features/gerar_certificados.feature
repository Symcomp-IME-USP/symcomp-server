#language:pt

Funcionalidade: Gerar Certificados
    Cenário: Uma pessoa não cadastrada gera um certificado 
        Dado que uma pessoa não está cadastrada, 
        Quando ela preenche com o seu nome e email
        Então deve ser gerado um certificado