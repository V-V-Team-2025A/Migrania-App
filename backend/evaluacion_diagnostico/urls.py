from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import EpisodioCefaleaViewSet

router = DefaultRouter()

router.register(
    r'evaluaciones/episodios',
    EpisodioCefaleaViewSet,
    basename='episodio-cefalea'
)

urlpatterns = [
    path('', include(router.urls)),
]