from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AtividadeView, RegisterView, EmailTokenObtainPairView, ValidateCodeView, PromoverUsuarioView, PalestranteView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("validate-code/", ValidateCodeView.as_view(), name="validate_code"),
    path('promover/', PromoverUsuarioView.as_view(), name='promover-usuario'),
    path("palestrante/", PalestranteView.as_view(), name='palestrante'),
    path("atividade/", AtividadeView.as_view(), name='atividade')
]
