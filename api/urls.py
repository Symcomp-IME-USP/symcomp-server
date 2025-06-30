from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PalestranteViewSet
from .views import RegisterView, EmailTokenObtainPairView

router = DefaultRouter()
router.register(r"palestrante", PalestranteViewSet, basename="palestrante")

urlpatterns = [
    path("", include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
