from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
from typing import List, Dict


User = get_user_model()


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
    total_episodios = serializers.IntegerField(min_value=1)
    suma_duracion_total = serializers.FloatField(min_value=0)


class DuracionPromedioEpisodiosResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para duración promedio"""
    duracion_promedio = serializers.FloatField()
    total_episodios = serializers.IntegerField()
    suma_duracion_total = serializers.FloatField()
    severidad = serializers.CharField()


class IntensidadPromedioDolorSerializer(serializers.Serializer):
    """Serializer para intensidad promedio del dolor"""
    intensidades = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=10),
        required=False,
        allow_empty=True
    )


class IntensidadPromedioDolorResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para intensidad promedio"""
    intensidad_promedio = serializers.CharField()
    gravedad = serializers.CharField()
    intensidades_procesadas = serializers.IntegerField()


class AsociacionHormonalSerializer(serializers.Serializer):
    """Serializer para asociación hormonal"""
    total_episodios = serializers.IntegerField(min_value=1)
    episodios_menstruacion = serializers.IntegerField(min_value=0)
    episodios_anticonceptivos = serializers.IntegerField(min_value=0)
    
    def validate(self, data):
        total = data['total_episodios']
        menstruacion = data['episodios_menstruacion']
        anticonceptivos = data['episodios_anticonceptivos']
        
        if menstruacion > total:
            raise serializers.ValidationError("Episodios menstruación no puede ser mayor al total")
        if anticonceptivos > total:
            raise serializers.ValidationError("Episodios anticonceptivos no puede ser mayor al total")
        
        return data


class AsociacionHormonalResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para asociación hormonal"""
    porcentaje_menstruacion = serializers.FloatField()
    porcentaje_anticonceptivos = serializers.FloatField()
    correlacion_menstruacion = serializers.CharField()
    correlacion_anticonceptivos = serializers.CharField()
    total_episodios = serializers.IntegerField()


class EvolucionMIDASSerializer(serializers.Serializer):
    """Serializer para evolución MIDAS"""
    puntuacion_promedio = serializers.FloatField(min_value=0)
    puntuacion_actual = serializers.FloatField(min_value=0)


class EvolucionMIDASResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para evolución MIDAS"""
    puntuacion_promedio = serializers.FloatField()
    puntuacion_actual = serializers.FloatField()
    diferencia = serializers.FloatField()
    tendencia = serializers.CharField()
    significancia = serializers.CharField()


class DesencadenantesFrecuenciaSerializer(serializers.Serializer):
    """Serializer para frecuencia de desencadenantes"""
    desencadenante = serializers.CharField()
    frecuencia = serializers.IntegerField()
    porcentaje = serializers.FloatField()
    relevancia = serializers.CharField()


class DesencadenantesComunesSerializer(serializers.Serializer):
    """Serializer para desencadenantes comunes"""
    desencadenantes = serializers.DictField(
        child=serializers.IntegerField(min_value=0)
    )
    
    def validate_desencadenantes(self, value):
        if not value:
            raise serializers.ValidationError("Debe proporcionar al menos un desencadenante")
        return value


class DesencadenantesComunesResponseSerializer(serializers.Serializer):
    """Serializer de respuesta para desencadenantes comunes"""
    desencadenantes_frecuentes = DesencadenantesFrecuenciaSerializer(many=True)
    total_menciones = serializers.IntegerField()
    cantidad_desencadenantes = serializers.IntegerField()


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
