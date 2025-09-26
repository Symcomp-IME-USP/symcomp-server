from desafio.questao.models import Questao

class ValidadorDeQuestoes:
    @staticmethod
    def validar_questao(questao: Questao, resposta: str) -> bool:
        return questao.resposta.strip().lower() == resposta.strip().lower()


class GerenciadorDePontuacao:
    @staticmethod
    def atualizar_pontuacao(usuario, questao: Questao, resposta: str) -> bool:
        correta = ValidadorDeQuestoes.validar_questao(questao, resposta)
        if correta:
            jogador = usuario.jogador
            jogador.pontos += int(questao.valor_pontos)
            jogador.save()
        return correta
