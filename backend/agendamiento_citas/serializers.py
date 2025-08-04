# citas/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError
from datetime import datetime, date, time
from .models import Cita, Recordatorio, Discapacidad
from usuarios.models import Usuario


class CitaListSerializer(serializers.ModelSerializer):
    """Serializer para listar citas (información resumida)"""
    doctor_nombre = serializers.CharField(source='doctor.get_full_name', read_only=True)
    paciente_nombre = serializers.CharField(source='paciente.get_full_name', read_only=True)
    fecha_hora_completa = serializers.DateTimeField(read_only=True)
    puede_cancelarse = serializers.BooleanField(read_only=True)
    puede_reprogramarse = serializers.BooleanField(read_only=True)

    class Meta:
        model = Cita
        fields = [
            'id', 'fecha', 'hora', 'estado', 'urgente',
            'doctor_nombre', 'paciente_nombre', 'fecha_hora_completa',
            'puede_cancelarse', 'puede_reprogramarse', 'creada_en'
        ]


class CitaDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle completo de citas"""
    doctor_nombre = serializers.CharField(source='doctor.get_full_name', read_only=True)
    paciente_nombre = serializers.CharField(source='paciente.get_full_name', read_only=True)
    doctor_info = serializers.SerializerMethodField()
    paciente_info = serializers.SerializerMethodField()
    fecha_hora_completa = serializers.DateTimeField(read_only=True)
    puede_cancelarse = serializers.BooleanField(read_only=True)
    puede_reprogramarse = serializers.BooleanField(read_only=True)

    class Meta:
        model = Cita
        fields = [
            'id', 'doctor', 'paciente', 'fecha', 'hora', 'estado', 'urgente',
            'motivo', 'observaciones', 'creada_en', 'doctor_nombre', 'paciente_nombre',
            'doctor_info', 'paciente_info', 'fecha_hora_completa',
            'puede_cancelarse', 'puede_reprogramarse'
        ]
        read_only_fields = ['id', 'creada_en']

    def get_doctor_info(self, obj):
        return {
            'id': obj.doctor.id,
            'nombre': obj.doctor.get_full_name(),
            'email': obj.doctor.email,
            'especialidad': getattr(obj.doctor, 'especialidad', None)
        }

    def get_paciente_info(self, obj):
        return {
            'id': obj.paciente.id,
            'nombre': obj.paciente.get_full_name(),
            'email': obj.paciente.email,
            'telefono': getattr(obj.paciente, 'telefono', None)
        }


class CitaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear citas"""
    doctor_id = serializers.IntegerField(write_only=True)
    paciente_id = serializers.IntegerField(write_only=True)
    fecha = serializers.DateField()
    hora = serializers.TimeField()

    class Meta:
        model = Cita
        fields = [
            'doctor_id', 'paciente_id', 'fecha', 'hora',
            'urgente', 'motivo', 'observaciones'
        ]

    def validate_doctor_id(self, value):
        try:
            doctor = Usuario.objects.get(id=value, tipo_usuario=Usuario.TipoUsuario.MEDICO)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Doctor no encontrado o no válido")

    def validate_paciente_id(self, value):
        try:
            paciente = Usuario.objects.get(id=value, tipo_usuario=Usuario.TipoUsuario.PACIENTE)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Paciente no encontrado o no válido")

    def validate(self, attrs):
        fecha = attrs.get('fecha')
        hora = attrs.get('hora')

        if fecha and hora:
            fecha_hora = datetime.combine(fecha, hora)
            if fecha_hora <= datetime.now():
                raise serializers.ValidationError("No se pueden agendar citas en el pasado")

        return attrs


class CitaUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar citas"""

    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'estado', 'motivo', 'observaciones', 'urgente']

    def validate(self, attrs):
        fecha = attrs.get('fecha', self.instance.fecha)
        hora = attrs.get('hora', self.instance.hora)

        if fecha and hora:
            fecha_hora = datetime.combine(fecha, hora)
            if fecha_hora <= datetime.now():
                raise serializers.ValidationError("No se pueden programar citas en el pasado")

        return attrs


class CitaUrgenteSerializer(serializers.Serializer):
    """Serializer para crear citas urgentes"""
    paciente_id = serializers.IntegerField()
    motivo = serializers.CharField(max_length=500, required=False, default="Atención médica urgente")

    def validate_paciente_id(self, value):
        try:
            Usuario.objects.get(id=value, tipo_usuario=Usuario.TipoUsuario.PACIENTE)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Paciente no encontrado o no válido")


class HorariosDisponiblesSerializer(serializers.Serializer):
    """Serializer para consultar horarios disponibles"""
    doctor_id = serializers.IntegerField()
    fecha = serializers.DateField()

    def validate_doctor_id(self, value):
        try:
            Usuario.objects.get(id=value, tipo_usuario=Usuario.TipoUsuario.MEDICO)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Doctor no encontrado")

    def validate_fecha(self, value):
        if value < date.today():
            raise serializers.ValidationError("No se puede consultar fechas pasadas")
        return value


class RecordatorioListSerializer(serializers.ModelSerializer):
    """Serializer para listar recordatorios"""
    paciente_nombre = serializers.CharField(source='paciente.get_full_name', read_only=True)
    cita_info = serializers.SerializerMethodField()
    fecha_hora_completa = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Recordatorio
        fields = [
            'id', 'tipo', 'fecha', 'hora', 'mensaje', 'enviado',
            'paciente_nombre', 'cita_info', 'fecha_hora_completa',
            'creado_en', 'enviado_en'
        ]

    def get_cita_info(self, obj):
        if obj.cita:
            return {
                'id': obj.cita.id,
                'fecha': obj.cita.fecha,
                'hora': obj.cita.hora,
                'doctor': obj.cita.doctor.get_full_name()
            }
        return None


class RecordatorioDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle completo de recordatorios"""
    paciente_info = serializers.SerializerMethodField()
    cita_info = serializers.SerializerMethodField()
    fecha_hora_completa = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Recordatorio
        fields = [
            'id', 'paciente', 'cita', 'tipo', 'fecha', 'hora', 'mensaje',
            'enviado', 'creado_en', 'enviado_en', 'paciente_info',
            'cita_info', 'fecha_hora_completa'
        ]
        read_only_fields = ['id', 'creado_en', 'enviado_en']

    def get_paciente_info(self, obj):
        return {
            'id': obj.paciente.id,
            'nombre': obj.paciente.get_full_name(),
            'email': obj.paciente.email
        }

    def get_cita_info(self, obj):
        if obj.cita:
            return {
                'id': obj.cita.id,
                'fecha': obj.cita.fecha,
                'hora': obj.cita.hora,
                'doctor': obj.cita.doctor.get_full_name(),
                'estado': obj.cita.estado
            }
        return None


class RecordatorioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear recordatorios"""
    paciente_id = serializers.IntegerField(write_only=True)
    cita_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Recordatorio
        fields = [
            'paciente_id', 'cita_id', 'tipo', 'fecha', 'hora', 'mensaje'
        ]

    def validate_paciente_id(self, value):
        try:
            Usuario.objects.get(id=value, tipo_usuario=Usuario.TipoUsuario.PACIENTE)
            return value
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Paciente no encontrado")

    def validate_cita_id(self, value):
        if value:
            try:
                Cita.objects.get(id=value)
                return value
            except Cita.DoesNotExist:
                raise serializers.ValidationError("Cita no encontrada")
        return value

    def validate(self, attrs):
        fecha = attrs.get('fecha')
        hora = attrs.get('hora')

        if fecha and hora:
            fecha_hora = datetime.combine(fecha, hora)
            if fecha_hora <= datetime.now():
                raise serializers.ValidationError("No se pueden programar recordatorios en el pasado")

        return attrs


class DiscapacidadSerializer(serializers.Serializer):
    """Serializer para manejar opciones de discapacidad"""
    value = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {
            'value': instance[0],
            'label': instance[1]
        }


class EstadisticasCitasSerializer(serializers.Serializer):
    """Serializer para estadísticas de citas"""
    total_citas = serializers.IntegerField()
    citas_pendientes = serializers.IntegerField()
    citas_confirmadas = serializers.IntegerField()
    citas_completadas = serializers.IntegerField()
    citas_canceladas = serializers.IntegerField()
    citas_urgentes = serializers.IntegerField()


class ReprogramarCitaSerializer(serializers.Serializer):
    """Serializer para reprogramar citas"""
    nueva_fecha = serializers.DateField()
    nueva_hora = serializers.TimeField()
    motivo = serializers.CharField(max_length=200, required=False)

    def validate(self, attrs):
        nueva_fecha = attrs.get('nueva_fecha')
        nueva_hora = attrs.get('nueva_hora')

        if nueva_fecha and nueva_hora:
            fecha_hora = datetime.combine(nueva_fecha, nueva_hora)
            if fecha_hora <= datetime.now():
                raise serializers.ValidationError("No se puede reprogramar a una fecha pasada")

        return attrs


class CancelarCitaSerializer(serializers.Serializer):
    """Serializer para cancelar citas"""
    motivo = serializers.CharField(max_length=200, required=False, default="")