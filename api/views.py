from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Palestrante
from .serializers import PalestranteSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView

class PalestranteViewSet(viewsets.ModelViewSet):
    queryset = Palestrante.objects.filter(active=True)
    serializer_class = PalestranteSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if User.objects.filter(username=data["username"]).exists():
            return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"]
        )
        return Response({"message": "Usuário criado"}, status=status.HTTP_201_CREATED)
