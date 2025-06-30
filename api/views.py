from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Palestrante, User, EmailVerificationCode
from .serializers import PalestranteSerializer, EmailTokenObtainPairSerializer
from rest_framework.views import APIView
from django.core.mail import send_mail
import random

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
        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Usuário já existe"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            name=data["name"],
            email=data["email"],
            password=data["password"]
        )
        
        code = f"{random.randint(100000, 999999)}"
        
        EmailVerificationCode.objects.create(user=user, code=code)
        
        send_mail(
            subject="Seu código de validação",
            message=f"Olá {user.name}, seu código de validação é: {code}",
            from_email="noreply@seusite.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        return Response({"message": "Usuário criado. Código de validação enviado por e-mail."}, status=status.HTTP_201_CREATED)

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
