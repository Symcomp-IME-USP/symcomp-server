from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PalestranteViewSet

router = DefaultRouter()
router.register(r"palestrante", PalestranteViewSet, basename="palestrante")

urlpatterns = [
    path("", include(router.urls)),
]
