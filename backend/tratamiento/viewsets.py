from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tratamiento
from .serializers import (
    TratamientoCreateSerializer,
    TratamientoSerializer,
    TratamientoResumenSerializer,
    TratamientoCancelarSerializer,
    TratamientoUpdateSerializer

)
from .TratamientoService import TratamientoService
from .permissions import (
    EsMedico,
    EsPaciente,
    EsPropietarioDelTratamientoOPersonalMedico,
)


class TratamientoViewSet(viewsets.ModelViewSet):
    queryset = Tratamiento.objects.all().order_by('-fecha_inicio')

    def get_serializer_class(self):
        if self.action == 'create':
            return TratamientoCreateSerializer
        elif self.action == 'cancelar':
            return TratamientoCancelarSerializer
        elif self.action == 'update' or self.action == 'partial_update' or self.action == 'modificar':
            return TratamientoUpdateSerializer
        elif self.action == 'historial':
            return TratamientoResumenSerializer
        else:
            return TratamientoSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [EsMedico()]
        elif self.action in ['update', 'partial_update', 'destroy', 'modificar', 'cancelar']:
            return [EsMedico()]
        elif self.action in ['confirmar_toma', 'mis_tratamientos_activos', 'primera_consulta']:
            return [EsPaciente()]
        else:  # list, retrieve, seguimiento, historial
            return [EsPropietarioDelTratamientoOPersonalMedico()]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['put'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        tratamiento = self.get_object()
        serializer = self.get_serializer(tratamiento, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save(activo=False, motivo_cancelacion=serializer.validated_data.get('motivo_cancelacion'))
        TratamientoService.cancelar_notificaciones(tratamiento)

        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='modificar')
    def modificar(self, request, pk=None):
        tratamiento = self.get_object()
        serializer = self.get_serializer(tratamiento, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        TratamientoService.cancelar_notificaciones(tratamiento)

        return Response(TratamientoSerializer(tratamiento).data)

    @action(detail=False, methods=['get'], url_path='historial/(?P<paciente_id>[^/.]+)')
    def historial(self, request, paciente_id=None):
        tratamientos = Tratamiento.objects.filter(paciente_id=paciente_id).order_by('-fecha_inicio')
        serializer = self.get_serializer(tratamientos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='primera-consulta/(?P<paciente_id>[^/.]+)')
    def primera_consulta(self, request, paciente_id=None):
        ultimo_tratamiento = Tratamiento.objects.filter(paciente_id=paciente_id).order_by('-fecha_inicio').first()
        data = {
            'num_episodio': ultimo_tratamiento.id if ultimo_tratamiento else None,
            'tipo_episodio': getattr(ultimo_tratamiento, 'tipo_migraña', None),
            'fecha': ultimo_tratamiento.fecha_inicio if ultimo_tratamiento else None,
        }
        return Response(data)

    @action(detail=False, methods=['get'], url_path='seguimiento/(?P<paciente_id>[^/.]+)')
    def seguimiento(self, request, paciente_id=None):
        tratamiento = Tratamiento.objects.filter(paciente_id=paciente_id, activo=True).order_by('-fecha_inicio').first()
        if not tratamiento:
            return Response({'estado': 'Sin tratamiento activo'}, status=status.HTTP_200_OK)

        data = {
            'num_episodio': tratamiento.id,
            'tipo_episodio': getattr(tratamiento, 'tipo_migraña', None),
            'fecha': tratamiento.fecha_inicio,
            'estado': 'Activo',
            'cumplimiento': tratamiento.cumplimiento,
        }
        return Response(data)