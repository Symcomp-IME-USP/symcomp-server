from rest_framework import serializers
from desafio.models import Desafio
from desafio.questao.serializers import QuestaoSerializer

class DesafioSerializer(serializers.ModelSerializer):
    questoes = QuestaoSerializer(many=True)

    class Meta:
        model = Desafio
        fields = "__all__"