#language: pt

Funcionalidade: Adicionar atividades no cronograma da Semana da Computação
    Cenário: Um organizador deve conseguir adicionar no cronograma uma atividade
        Dado que Odair é organizador
        Quando ele adiciona uma atividade no cronograma
        Então a atividade deve ser adicionada

    Cenário: Um usuário que não é organizador não deve conseguir adicionar uma atividade no cronograma
        Dado que Carlinhos não é um organizador
        Quando ele tenta adicionar uma atividade no cronograma
        Então a atividade não deve ser adicionada

    Cenário: Um organizador não deve poder adicionar uma atividade fora dos horários do cronograma
        Dado que Odair é organizador
        Quando ele adicionar uma atividade fora dos dias 20 a 24 de outubro
        E fora do horário das 12:00 às 18:45
        Então a atividade não deve ser adicionada

    Cenário: Um organizador não deve poder adicionar uma atividade que não está livre no cronograma
        Dado que Odair é organizador
        Quando ele adicionar uma atividade na segunda feira às 12:00
        E adiciona outra atividade no mesmo horário da segunda feira às 12:00
        Então só deve ser adicionada uma atividade

    Cenário: Um QR code deve ser gerado automaticamente ao criar uma atividade
        Dado que Odair é organizador
        Quando ele adiciona uma atividade no cronograma
        Então um QR code deve ser gerado para a atividade