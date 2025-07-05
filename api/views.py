from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import Palestrante, User, EmailVerificationCode
from .serializers import (
    PalestranteSerializer,
    EmailTokenObtainPairSerializer,
    RegisterSerializer
)
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
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        if User.objects.filter(email=email).exists():
            return Response({"error": "Usuário já existe"}, status=status.HTTP_409_CONFLICT)

        user = serializer.save()
        
        code = f"{random.randint(100000, 999999)}"
        EmailVerificationCode.objects.create(user=user, code=code)

        send_mail(
            subject="Seu código de validação",
            message=f"Olá {user.name}, seu código de validação é: {code}",
            from_email="noreply@symcomp.ime.usp.br",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Usuário criado. Código de validação enviado por e-mail."},
            status=status.HTTP_201_CREATED
        )

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class ValidateCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        try:
            evc = EmailVerificationCode.objects.filter(user=user, code=code, is_used=False).latest("created_at")
        except EmailVerificationCode.DoesNotExist:
            return Response({"error": "Código inválido ou expirado"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        evc.is_used = True
        evc.save()

        return Response({"message": "Usuário validado com sucesso"}, status=status.HTTP_200_OK)
