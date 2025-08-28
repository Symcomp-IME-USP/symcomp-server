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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AtividadeView, RegisterView, EmailTokenObtainPairView, ValidateCodeView, PromoverUsuarioView, PalestranteView, RefreshAccessTokenView, CertificateView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh_cookie'),
    path("validate-code/", ValidateCodeView.as_view(), name="validate_code"),
    path('promover/', PromoverUsuarioView.as_view(), name='promover-usuario'),
    path("palestrante/", PalestranteView.as_view(), name='palestrante'),
    path("atividade/", AtividadeView.as_view(), name='atividade'),
    path("certificado/", CertificateView.as_view(), name='certificado')
]
