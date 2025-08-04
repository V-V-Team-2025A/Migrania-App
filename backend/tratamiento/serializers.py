from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Tratamiento, Medicamento, Recomendacion, EstadoNotificacion
from .permissions import EsMedico, EsPaciente, EsPropietarioDelTratamientoOPersonalMedico
from .services import TratamientoService

class MedicamentoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = [
            'nombre', 'dosis', 'caracteristica',
            'frecuencia_horas', 'duracion_dias', 'hora_de_inicio'
        ]


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = [
            'id', 'nombre', 'dosis', 'caracteristica',
            'frecuencia_horas', 'duracion_dias', 'hora_de_inicio'
        ]


class TratamientoCreateSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoCreateSerializer(many=True)
    recomendaciones = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    paciente = serializers.PrimaryKeyRelatedField(queryset=None)  # Asignar queryset en init si quieres

    class Meta:
        model = Tratamiento
        fields = ['episodio', 'paciente', 'medicamentos', 'recomendaciones']

    def create(self, validated_data):
        medicamentos_data = validated_data.pop('medicamentos', [])
        recomendaciones_ids = validated_data.pop('recomendaciones', [])
        tratamiento = Tratamiento.objects.create(**validated_data)

        for med_data in medicamentos_data:
            medicamento = Medicamento.objects.create(**med_data)
            tratamiento.medicamentos.add(medicamento)

        tratamiento.recomendaciones.set(recomendaciones_ids)
        return tratamiento


class TratamientoCancelarSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoSerializer(many=True, read_only=True)
    porcentaje_cumplimiento = serializers.FloatField(source='cumplimiento', read_only=True)

    class Meta:
        model = Tratamiento
        fields = ['id', 'medicamentos', 'porcentaje_cumplimiento', 'motivo_cancelacion']


class TratamientoUpdateSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoCreateSerializer(many=True, required=False)
    recomendaciones = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

    class Meta:
        model = Tratamiento
        fields = ['episodio', 'medicamentos', 'recomendaciones']

    def update(self, instance, validated_data):
        medicamentos_data = validated_data.pop('medicamentos', None)
        recomendaciones_ids = validated_data.pop('recomendaciones', None)

        # Actualizar campos simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Actualizar medicamentos
        if medicamentos_data is not None:
            instance.medicamentos.clear()
            for med_data in medicamentos_data:
                medicamento = Medicamento.objects.create(**med_data)
                instance.medicamentos.add(medicamento)

        # Actualizar recomendaciones
        if recomendaciones_ids is not None:
            instance.recomendaciones.set(recomendaciones_ids)

        instance.save()
        return instance


class TratamientoResumenSerializer(serializers.ModelSerializer):
    episodio = serializers.CharField(source='episodio')
    porcentaje_cumplimiento = serializers.FloatField(source='cumplimiento')

    class Meta:
        model = Tratamiento
        fields = ['id', 'episodio', 'fecha_inicio', 'activo', 'porcentaje_cumplimiento']


class TratamientoSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoSerializer(many=True, read_only=True)
    recomendaciones = serializers.SerializerMethodField()
    paciente_nombre = serializers.CharField(source='paciente.usuario.get_full_name', read_only=True)

    class Meta:
        model = Tratamiento
        fields = [
            'id', 'episodio', 'paciente', 'paciente_nombre', 'fecha_inicio',
            'activo', 'cumplimiento', 'medicamentos', 'recomendaciones', 'motivo_cancelacion'
        ]

    def get_recomendaciones(self, obj):
        return [str(r) for r in obj.recomendaciones.all()]


# ViewSet

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
