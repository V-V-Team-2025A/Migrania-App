# analiticas/estadisticas_serializers.py
from rest_framework import serializers


class EstadisticasHistorialSerializer(serializers.Serializer):
    """
    Serializer para las estadísticas del historial de episodios de bitácora digital.
    """
    # Estadísticas de promedio semanal
    promedio_semanal = serializers.FloatField(
        required=False,
        help_text="Promedio semanal de episodios de migraña"
    )
    
    # Estadísticas de duración promedio
    duracion_promedio = serializers.FloatField(
        required=False,
        help_text="Duración promedio por episodio en horas"
    )
    
    # Estadísticas de intensidad promedio
    intensidad_promedio = serializers.CharField(
        required=False,
        help_text="Intensidad promedio del dolor (Leve, Moderado, Severo)"
    )
    
    # Estadísticas de asociación hormonal
    porcentaje_menstruacion = serializers.FloatField(
        required=False,
        help_text="Porcentaje de episodios durante menstruación"
    )
    porcentaje_anticonceptivos = serializers.FloatField(
        required=False,
        help_text="Porcentaje de episodios asociados a anticonceptivos"
    )
    
    # Información adicional
    total_episodios = serializers.IntegerField(
        required=False,
        help_text="Total de episodios registrados"
    )
    fecha_primer_episodio = serializers.DateField(
        required=False,
        help_text="Fecha del primer episodio registrado"
    )
    fecha_ultimo_episodio = serializers.DateField(
        required=False,
        help_text="Fecha del último episodio registrado"
    )


class PromediaSemanalRequestSerializer(serializers.Serializer):
    """
    Serializer para los parámetros de solicitud de promedio semanal.
    """
    fecha_inicio = serializers.DateField(
        required=False,
        help_text="Fecha de inicio del período a analizar"
    )
    fecha_fin = serializers.DateField(
        required=False,
        help_text="Fecha de fin del período a analizar"
    )


class EvolucionMidasSerializer(serializers.Serializer):
    """
    Serializer para la evolución de puntuaciones MIDAS.
    """
    puntuacion_actual = serializers.FloatField(
        help_text="Puntuación MIDAS más reciente"
    )
    puntuacion_anterior = serializers.FloatField(
        help_text="Puntuación MIDAS anterior"
    )
    diferencia = serializers.FloatField(
        help_text="Diferencia entre puntuación actual y anterior"
    )
    tendencia = serializers.CharField(
        help_text="Tendencia: 'mejora', 'empeoramiento' o 'estable'"
    )
    interpretacion = serializers.CharField(
        help_text="Interpretación textual del cambio"
    )


class EstadisticasUnificadasSerializer(serializers.Serializer):
    """
    Serializer para el endpoint unificado de estadísticas.
    Combina estadísticas historial con evolución MIDAS.
    """
    paciente_id = serializers.IntegerField(
        help_text="ID del paciente"
    )
    total_episodios = serializers.IntegerField(
        help_text="Total de episodios registrados"
    )
    duracion_promedio = serializers.FloatField(
        required=False,
        help_text="Duración promedio por episodio en horas"
    )
    intensidad_promedio = serializers.FloatField(
        required=False,
        help_text="Intensidad promedio del dolor (escala 1-10)"
    )
    porcentaje_menstruacion = serializers.FloatField(
        required=False,
        help_text="Porcentaje de episodios durante menstruación"
    )
    porcentaje_anticonceptivos = serializers.FloatField(
        required=False,
        help_text="Porcentaje de episodios asociados a anticonceptivos"
    )
    evolucion_midas = EvolucionMidasSerializer(
        required=False,
        help_text="Evolución de la puntuación MIDAS"
    )
    
    # Campos para casos de datos insuficientes
    mensaje = serializers.CharField(
        required=False,
        help_text="Mensaje informativo cuando no hay suficientes datos"
    )
    datos_minimos_requeridos = serializers.DictField(
        required=False,
        help_text="Información sobre datos mínimos requeridos"
    )
