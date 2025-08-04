from rest_framework import viewsets, mixins, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Pregunta, Respuesta, AutoevaluacionMidas
from .permissions import EsPaciente, EsPropietarioDeLaAutoevaluacionOPersonalMedico
from .autoevaluacion_midas_service import autoevaluacion_midas_service

from .serializers import (
    PreguntaSerializer,
    CrearAutoevaluacionSerializer, AutoevaluacionMidasSerializer,
    CrearRespuestaSerializer, RespuestaSerializer,
)


class PreguntaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet para manejar las preguntas de la autoevaluación MIDAS.
    Permite listar y ver los detalles de las preguntas.
    """
    queryset = Pregunta.objects.all().order_by('orden_pregunta')
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAuthenticated]


class AutoevaluacionMidasViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las autoevaluaciones MIDAS.
    Permite crear, listar y ver autoevaluaciones.
    """
    queryset = AutoevaluacionMidas.objects.select_related("paciente").all()
    permission_classes = [permissions.IsAuthenticated, EsPropietarioDeLaAutoevaluacionOPersonalMedico]

    def get_serializer_class(self):
        """
        Devuelve el serializer adecuado según la acción.
        """
        if self.action == 'create':
            return CrearAutoevaluacionSerializer
        return AutoevaluacionMidasSerializer

    def get_queryset(self):
        user = self.request.user
        if user.es_medico or user.es_enfermera:
            return self.queryset
        return self.queryset.filter(paciente=user)

    def perform_create(self, serializer):
        """
        Guarda la autoevaluación MIDAS creada por el paciente.
        """
        paciente = self.request.user
        ultima = AutoevaluacionMidas.objects.filter(paciente=paciente).order_by('-fecha_autoevaluacion').first()
        if ultima:
            delta = serializer.validated_data.get("fecha_autoevaluacion") or ultima.fecha_autoevaluacion
            dias = (delta - ultima.fecha_autoevaluacion).days
            if dias < 90:
                raise PermissionDenied("Debes esperar al menos 90 días para una nueva autoevaluación.")
        serializer.save(paciente=paciente)


class RespuestaViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet para manejar las respuestas a las preguntas de la autoevaluación MIDAS.
    Permite crear respuestas y listar las respuestas de una autoevaluación específica.
    """
    queryset = Respuesta.objects.select_related('autoevaluacion', 'pregunta').all()
    serializer_class = RespuestaSerializer
    permission_classes = [permissions.IsAuthenticated, EsPaciente]

    def create(self, request, *args, **kwargs):
        """
        Crea una respuesta y, si es la última (pregunta 5), actualiza el puntaje total.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        respuesta = serializer.save()
        autoevaluacion = respuesta.autoevaluacion
        if autoevaluacion.respuestas_midas_individuales.count() == 5:
            # Actualiza el puntaje total y grado de discapacidad
            autoevaluacion.actualizar_puntaje_total()
        return Response(serializer.data)
