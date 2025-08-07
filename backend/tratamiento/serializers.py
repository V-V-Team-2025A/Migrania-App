from rest_framework import serializers
from .models import Tratamiento, Medicamento, Recomendacion, Alerta, Recordatorio, EstadoNotificacion


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
    # SOLUCIÓN: Definir el queryset directamente
    paciente = serializers.PrimaryKeyRelatedField(
        queryset=PacienteProfile.objects.all()
    )

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
    episodio = serializers.StringRelatedField(read_only=True)
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


class TratamientoSeguimientoSerializer(serializers.ModelSerializer):
    medicamentos = MedicamentoSerializer(many=True, read_only=True)

    class Meta:
        model = Tratamiento
        fields = ['id', 'medicamentos', 'cumplimiento', 'activo', 'fecha_inicio']

class TratamientoResumenSerializer(serializers.ModelSerializer):
    episodio = serializers.StringRelatedField()
    paciente = serializers.StringRelatedField()

    class Meta:
        model = Tratamiento
        fields = ['id', 'episodio', 'paciente', 'fecha_inicio', 'activo', 'cumplimiento']


class TratamientoCancelarSerializer(serializers.ModelSerializer):
    motivo_cancelacion = serializers.CharField(required=True)

    class Meta:
        model = Tratamiento
        fields = ['motivo_cancelacion']

class TratamientoHistorialSerializer(serializers.ModelSerializer):
    medicamentos_count = serializers.IntegerField(source='medicamentos.count', read_only=True)
    duracion = serializers.SerializerMethodField()

    def get_duracion(self, obj):
        return obj.calcularDuracion()

    class Meta:
        model = Tratamiento
        fields = [
            'id', 'fecha_inicio', 'activo', 'cumplimiento',
            'medicamentos_count', 'duracion', 'motivo_cancelacion'
        ]


class TratamientoCancelacionSerializer(serializers.ModelSerializer):
    motivo_cancelacion = serializers.CharField(required=True)

    class Meta:
        model = Tratamiento
        fields = ['motivo_cancelacion']


class NotificacionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    mensaje = serializers.CharField()
    fecha_hora = serializers.DateTimeField()
    estado = serializers.CharField()
    tipo = serializers.SerializerMethodField()

    def get_tipo(self, obj):
        return obj.__class__.__name__


class AlertaSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()

    class Meta:
        model = Alerta
        fields = ['id', 'mensaje', 'fecha_hora', 'estado', 'numero_alerta', 
                 'duracion', 'tiempo_espera', 'tipo']

    def get_tipo(self, obj):
        return 'Alerta'


class RecordatorioSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()

    class Meta:
        model = Recordatorio
        fields = ['id', 'mensaje', 'fecha_hora', 'estado', 'tipo']

    def get_tipo(self, obj):
        return 'Recordatorio'


class CambiarEstadoAlertaSerializer(serializers.Serializer):
    nuevo_estado = serializers.ChoiceField(
        choices=[
            ('tomado', 'Confirmado Tomado'),
            ('no_tomado', 'Confirmado No Tomado'),
            ('tomado_tarde', 'Confirmado Tomado Tarde'),
            ('tomado_muy_tarde', 'Confirmado Tomado Muy Tarde'),
        ]
    )
    hora_confirmacion = serializers.DateTimeField(required=False)


class NotificacionesPendientesSerializer(serializers.Serializer):
    alertas = AlertaSerializer(many=True)
    recordatorios = RecordatorioSerializer(many=True)
    total = serializers.IntegerField()
