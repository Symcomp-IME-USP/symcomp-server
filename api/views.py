from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import PerfilUsuario, Papel, User, Atividade, EmailVerificationCode, Palestrante
from .serializers import (
    EmailTokenObtainPairSerializer,
    RegisterSerializer,
    PalestranteSerializer,
    AtividadeSerializer
)
import random
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

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

class PromoverUsuarioView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'erro': 'Autenticação necessária.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            perfil_solicitante = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            return Response({'erro': 'Usuário sem perfil.'}, status=status.HTTP_403_FORBIDDEN)

        if perfil_solicitante.papel not in [Papel.ORGANIZADOR, Papel.PRESIDENTE]:
            return Response({'erro': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

        email_alvo = request.data.get('email')
        novo_papel = request.data.get('papel')

        if novo_papel not in Papel.values:
            return Response({'erro': 'Papel inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        if novo_papel == Papel.PRESIDENTE and perfil_solicitante.papel != Papel.PRESIDENTE:
            return Response({'erro': 'Apenas presidentes podem promover para presidente.'}, status=status.HTTP_403_FORBIDDEN)

        user_alvo = get_object_or_404(User, email=email_alvo)
        perfil_alvo, _ = PerfilUsuario.objects.get_or_create(user=user_alvo)

        perfil_alvo.papel = novo_papel
        perfil_alvo.save()

        return Response({'mensagem': f'{email_alvo} promovido para {novo_papel}.'}, status=status.HTTP_200_OK)

class PalestranteView(APIView):
    def get(self, request):
        palestrantes = Palestrante.objects.all()
        serializer = PalestranteSerializer(palestrantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PalestranteSerializer(data=request.data)
        if serializer.is_valid():
            palestrante = serializer.save()

            code = f"{random.randint(100000, 999999)}"
            send_mail(
                subject="Seu código de primeiro acesso",
                message=f"Olá {palestrante.display_name}, seu código de validação é: {code}",
                from_email="noreply@symcomp.ime.usp.br",
                recipient_list=[palestrante.email],
                fail_silently=False,
            )

            return Response(PalestranteSerializer(palestrante).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AtividadeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        atividades = Atividade.objects.all()
        serializer = AtividadeSerializer(atividades, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AtividadeSerializer(data=request.data)

        if not request.user.is_authenticated:
            return Response({'erro': 'Autenticação necessária.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            perfil_solicitante = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            return Response({'erro': 'Usuário sem perfil'}, status=status.HTTP_403_FORBIDDEN)

        if perfil_solicitante.papel not in [Papel.ORGANIZADOR, Papel.PRESIDENTE]:
            return Response({'erro': 'Permissão negada.'}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            atividade = serializer.save()
            return Response(AtividadeSerializer(atividade).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    