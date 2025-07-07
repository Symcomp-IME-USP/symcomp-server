#language: pt

Funcionalidade: Criar um cronograma
    Cenário: O presidente do grupo cria um cronograma
        Dado que Odair é o presidente do grupo
        Quando ele fornece corretamente as informações sobre o cronograma
        Então deve ser possível cadastrar uma palestra no intervalo especificado
        E não pode ser possível cadastrar uma palestra nas pausas

    Cenário: O presidente do grupo define os horários de coffee break
        Dado que Anna é presidente do grupo
        Quando ela define um horário de coffee break
        Então, todos os dias do período definido devem estar bloqueadas de realizar palestra

    Cenário: O presidente do grupo modifica detalhes do horário cronograma
        Dado que Odair é o presidente do grupo
        Quando ele modifica o horário do cronograma
        E salva as alterações
        Então as palestras devem sofrer alteração de horário correspondente à alteração do cronograma
