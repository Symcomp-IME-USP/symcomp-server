from rest_framework import viewsets
from .models import Palestrante
from .serializers import PalestranteSerializer

class PalestranteViewSet(viewsets.ModelViewSet):
    queryset = Palestrante.objects.all()
    serializer_class = PalestranteSerializer
