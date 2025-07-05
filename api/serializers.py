from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .validators import validate_strong_password
from .models import Palestrante, Link, User

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["domain", "url"]

class PalestranteSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, required=False)

    class Meta:
        model = Palestrante
        fields = [
            "id", "nome", "ocupacao", "biografia", "email",
            "link_apresentacao", "foto_url", "foto_alt", "links"
        ]
        read_only_fields = ["id"]


    def create(self, validated_data):
        links_data = validated_data.pop("links")
        palestrante = Palestrante.objects.create(**validated_data)
        for link_data in links_data:
            link, _ = Link.objects.get_or_create(**link_data)
            palestrante.links.add(link)
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
