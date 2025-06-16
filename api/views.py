from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Palestrante
from .serializers import PalestranteSerializer

class PalestranteViewSet(viewsets.ModelViewSet):
    queryset = Palestrante.objects.filter(active=True)
    serializer_class = PalestranteSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

