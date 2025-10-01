from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from desafio.questao.models import Questao
from desafio.services import GerenciadorDePontuacao

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def responder_questao(request, questao_id):
    """
    Recebe a resposta do usuário, valida e atualiza a pontuação.
    """
    try:
        questao = Questao.objects.get(id=questao_id)
    except Questao.DoesNotExist:
        return Response({"error": "Questão não encontrada"}, status=404)

    resposta_usuario = request.data.get("resposta")
    if resposta_usuario is None:
        return Response({"error": "Resposta não fornecida"}, status=400)

    correta = GerenciadorDePontuacao.atualizar_pontuacao(request.user, questao, resposta_usuario)

    return Response({
        "questao": questao.pergunta,
        "resposta_correta": correta,
        "pontuacao_atual": request.user.jogador.pontos
    })
