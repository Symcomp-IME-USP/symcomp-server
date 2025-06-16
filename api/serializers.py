from rest_framework import serializers
from .models import Palestrante, Link

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
