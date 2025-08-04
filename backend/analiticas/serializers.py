# analiticas/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
from typing import List, Dict


User = get_user_model()


class AnalisisPatronesSerializer(serializers.Serializer):
    """
    Serializador para empaquetar todas las conclusiones del análisis.
    """
    conclusion_clinica = serializers.CharField()
    conclusiones_sintomas = serializers.DictField()
    conclusion_aura = serializers.CharField()
    dias_recurrentes = serializers.ListField(child=serializers.CharField())
    conclusion_hormonal = serializers.CharField()


# Serializers para Estadísticas Historial
class PromedioSemanalEpisodiosSerializer(serializers.Serializer):
    """Serializer para promedio semanal de episodios"""
    total_episodios = serializers.IntegerField(min_value=0)
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    
    def validate(self, data):
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha fin")
        return data


class PromedioSemanalEpisodiosResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para promedio semanal"""
    promedio_semanal = serializers.FloatField()
    total_episodios = serializers.IntegerField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    interpretacion = serializers.CharField()


class DuracionPromedioEpisodiosSerializer(serializers.Serializer):
    """Serializer para duración promedio de episodios"""
    total_episodios = serializers.IntegerField(min_value=0)
    suma_duracion_total = serializers.FloatField(min_value=0.0)


class DuracionPromedioEpisodiosResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para duración promedio"""
    duracion_promedio = serializers.FloatField()
    total_episodios = serializers.IntegerField()
    interpretacion = serializers.CharField()


class IntensidadPromedioDolor_InputSerializer(serializers.Serializer):
    """Serializer para entrada de intensidades de dolor"""
    intensidades = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=10),
        allow_empty=True,
        required=False
    )
    
    def validate_intensidades(self, value):
        if value and len(value) > 1000:  # Límite razonable
            raise serializers.ValidationError("Demasiadas intensidades proporcionadas")
        return value


class IntensidadPromedioDolor_ResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para intensidad promedio"""
    intensidad_promedio = serializers.CharField()
    descripcion = serializers.CharField()


class AsociacionHormonalSerializer(serializers.Serializer):
    """Serializer para asociación hormonal"""
    total_episodios = serializers.IntegerField(min_value=0)
    episodios_menstruacion = serializers.IntegerField(min_value=0)
    episodios_anticonceptivos = serializers.IntegerField(min_value=0)
    
    def validate(self, data):
        if data['episodios_menstruacion'] > data['total_episodios']:
            raise serializers.ValidationError("Los episodios durante menstruación no pueden ser más que el total")
        if data['episodios_anticonceptivos'] > data['total_episodios']:
            raise serializers.ValidationError("Los episodios con anticonceptivos no pueden ser más que el total")
        return data


class AsociacionHormonalResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para asociación hormonal"""
    porcentaje_menstruacion = serializers.FloatField()
    porcentaje_anticonceptivos = serializers.FloatField()
    interpretacion_menstruacion = serializers.CharField()
    interpretacion_anticonceptivos = serializers.CharField()


class EvolucionMIDASSerializer(serializers.Serializer):
    """Serializer para evolución MIDAS"""
    puntuacion_promedio = serializers.FloatField(min_value=0.0)
    puntuacion_actual = serializers.FloatField(min_value=0.0)


class EvolucionMIDASResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para evolución MIDAS"""
    categoria_promedio = serializers.CharField()
    categoria_actual = serializers.CharField()
    tendencia = serializers.CharField()
    interpretacion = serializers.CharField()


class DesencadenanesComunes_InputSerializer(serializers.Serializer):
    """Serializer para entrada de desencadenantes comunes"""
    desencadenantes_dict = serializers.DictField(
        child=serializers.IntegerField(min_value=0),
        allow_empty=False
    )
    
    def validate_desencadenantes_dict(self, value):
        if len(value) > 50:  # Límite razonable de desencadenantes
            raise serializers.ValidationError("Demasiados tipos de desencadenantes")
        return value


class DesencadenanesComunes_ResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para desencadenantes comunes"""
    desencadenantes_frecuentes = serializers.ListField(
        child=serializers.DictField()
    )
    interpretacion = serializers.CharField()


class EstadisticasHistorialCompletasSerializer(serializers.Serializer):
    """Serializer para estadísticas historial completas"""
    promedio_semanal = PromedioSemanalEpisodiosResponseSerializer()
    duracion_promedio = DuracionPromedioEpisodiosResponseSerializer()
    intensidad_promedio = IntensidadPromedioDolor_ResponseSerializer()
    asociacion_hormonal = AsociacionHormonalResponseSerializer()
    evolucion_midas = EvolucionMIDASResponseSerializer()
    desencadenantes_comunes = DesencadenanesComunes_ResponseSerializer()


class EstadisticaGeneralSerializer(serializers.Serializer):
    """Serializer general para todas las estadísticas"""
    tipo_estadistica = serializers.ChoiceField(choices=[
        'promedio_semanal',
        'duracion_promedio', 
        'intensidad_promedio',
        'asociacion_hormonal',
        'evolucion_midas',
        'desencadenantes_comunes'
    ])
    datos = serializers.JSONField()
