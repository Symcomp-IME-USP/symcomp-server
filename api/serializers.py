from datetime import time, date
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .validators import validate_strong_password
from .models import Palestrante, Link, User, PerfilUsuario, Papel, Atividade, ActivityHistory

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["domain", "url"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_strong_password],
        error_messages={
            "blank": "A senha não pode ser vazia.",
            "required": "O campo senha é obrigatório."
        },
        max_length=255,
        allow_blank=False
    )

    class Meta:
        model = User
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        return super().validate(attrs)
    
class PalestranteSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, required=False)

    class Meta:
        model = Palestrante
        fields = [
            "id", "email", "display_name", "ocupacao", "biografia",
            "link_apresentacao", "foto_url", "foto_alt", "links"
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        links_data = validated_data.pop("links", [])

        palestrante = Palestrante.objects.create(**validated_data)

        for link_data in links_data:
            link, _ = Link.objects.get_or_create(**link_data)
            palestrante.links.add(link)

        try:
            user = User.objects.get(email=palestrante.email)
            perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
            if perfil.papel != Papel.PALESTRANTE:
                perfil.papel = Papel.PALESTRANTE
                perfil.save()
        except User.DoesNotExist:
            pass

        return palestrante

    def update(self, instance, validated_data):
        links_data = validated_data.pop("links", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if links_data is not None:
            instance.links.clear()
            for link_data in links_data:
                link, _ = Link.objects.get_or_create(**link_data)
                instance.links.add(link)

        return instance


class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = [
            "id", "tipo", "status", "comeca_as", "termina_as", "qr_code"
        ]
        read_only_fields = ["id", "qr_code"]

    def validate(self, validated_data):
        comeca_as = validated_data.get("comeca_as")
        termina_as = validated_data.get("termina_as")

        dia_min = date(comeca_as.year, 10, 20)
        dia_max = date(comeca_as.year, 10, 24)

        if not (dia_min <= comeca_as.date() <= dia_max):
            raise serializers.ValidationError("A atividade deve começar entre os dias 20 e 24 de outubro.")
        
        if not (dia_min <= termina_as.date() <= dia_max):
            raise serializers.ValidationError("A atividade deve terminar entre os dias 20 e 24 de outubro.")

        hora_min = time(12, 0)
        hora_max = time(18, 45)

        if not (hora_min <= comeca_as.time() <= hora_max):
            raise serializers.ValidationError("A atividade deve começar entre 12:00 e 18:45.")
        
        if not (hora_min <= termina_as.time() <= hora_max):
            raise serializers.ValidationError("A atividade deve terminar entre 12:00 e 18:45.")

        return validated_data

    def create(self, validated_data):
        return Atividade.objects.create(**validated_data)

class CertitificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityHistory
        fields = ['id', 'user', 'activity']

    def create(self, validated_data):
        return ActivityHistory.objects.create(**validated_data)