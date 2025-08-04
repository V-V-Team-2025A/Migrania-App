# evaluacion_diagnostico/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PreguntaViewSet, AutoevaluacionMidasViewSet, RespuestaViewSet

router = DefaultRouter()
router.register(r'evaluaciones/preguntas', PreguntaViewSet, basename='pregunta')
router.register(r'evaluaciones/autoevaluaciones', AutoevaluacionMidasViewSet, basename='autoevaluacion')
router.register(r'evaluaciones/respuestas', RespuestaViewSet, basename='respuesta')

urlpatterns = [
    path('', include(router.urls)),
]
