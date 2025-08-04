from datetime import datetime

from rest_framework import serializers
from .models import AutoevaluacionMidas, Pregunta, Respuesta


class PreguntaSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar las preguntas de la autoevaluación MIDAS.
    """

    class Meta:
        model = Pregunta
        fields = ['id', 'orden_pregunta', 'enunciado_pregunta']
        read_only_fields = ['id']


class CrearAutoevaluacionSerializer(serializers.ModelSerializer):
    """
    Serializer para crear una autoevaluación MIDAS.
    Permite que un paciente cree una nueva autoevaluación MIDAS.
    """

    class Meta:
        model = AutoevaluacionMidas
        fields = ['id', 'paciente', 'fecha_autoevaluacion']
        read_only_fields = ['id', 'paciente', 'fecha_autoevaluacion']


class CrearRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['autoevaluacion', 'pregunta', 'valor_respuesta']

    # TODO: revisar redundancia
    def validate(self, data):
        evaluacion = data.get('autoevaluacion')
        if evaluacion.respuestas_midas_individuales.count() >= 5:
            raise serializers.ValidationError("No se pueden registrar más de 5 respuestas.")
        return data


class RespuestaSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar las respuestas a las preguntas de la autoevaluación MIDAS.
    Permite ver las respuestas registradas en la autoevaluación MIDAS.
    """

    pregunta = PreguntaSerializer(read_only=True)

    class Meta:
        model = Respuesta
        fields = ['pregunta', 'valor_respuesta', 'respondido_en']


class AutoevaluacionMidasSerializer(serializers.ModelSerializer):
    """
    Serializer para mostrar los detalles de una autoevaluación MIDAS.
    Incluye el puntaje total, grado de discapacidad y las respuestas individuales.
    """

    respuestas_midas_individuales = RespuestaSerializer(many=True, read_only=True)
    fecha_autoevaluacion = serializers.SerializerMethodField()

    class Meta:
        model = AutoevaluacionMidas
        fields = ['id', 'fecha_autoevaluacion',
                  'puntaje_total', 'grado_discapacidad',
                  'respuestas_midas_individuales'
                  ]

    def get_fecha_autoevaluacion(self, obj):
        # Forzar a date en caso de que sea datetime
        if isinstance(obj.fecha_autoevaluacion, datetime):
            return obj.fecha_autoevaluacion.date()
        return obj.fecha_autoevaluacion
