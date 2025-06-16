from rest_framework import viewsets
from api.models import Palestrante
from api.serializers import PalestranteSerializer

class PalestranteViewSet(viewsets.ModelViewSet):
    queryset = Palestrante.objects.all()
    serializer_class = PalestranteSerializer