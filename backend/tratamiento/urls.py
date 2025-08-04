from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import TratamientoViewSet

router = DefaultRouter()
router.register(r'tratamientos',
    TratamientoViewSet,
    basename='tratamiento'
)
urlpatterns = [
    path('', include(router.urls)),
]