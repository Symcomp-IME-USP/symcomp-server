from rest_framework import serializers
from desafio.questao.models import Questao

class QuestaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questao
        fields = "__all__"