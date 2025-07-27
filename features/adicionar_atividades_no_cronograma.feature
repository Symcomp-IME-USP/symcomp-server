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

    Cenário: Um organizador não deve poder adicionar uma atividade fora dos dias do cronograma
        Dado que Odair é organizador
        Quando ele adicionar uma atividade fora do dia do cronograma
        Então a atividade não deve ser adicionada

    Cenário: Um organizador não deve poder adicionar uma atividade durante o coffee break
        Dado que Odair é organizador
        Quando ele adicionar uma atividade em qualquer um dos dias das 14:15 às 14:45 ou 18:15 às 18:45
        Então a atividade não deve ser adicionada

    Cenário: Um organizador não deve poder adicionar uma atividade durante o encerramento do evento
        Dado que Odair é organizador
        Quando ele adicionar uma atividade na sexta feira das 17:15 às 17:45
        Então a atividade não deve ser adicionada

    Cenário: Um organizador não deve poder adicionar uma atividade que não está livre no cronograma
        Dado que Odair é organizador
        Quando ele adicionar uma atividade na segunda feira às 17:15
        E adiciona outra atividade no mesmo horário da segunda feira às 17:15
        Então a atividade não deve ser adicionada