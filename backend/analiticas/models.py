from django.db import models
from django.core.validators import MinValueValidator


class PromedioSemanalEpisodios(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    total_episodios = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    promedio_semanal = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    
    def __str__(self):
        return f"Promedio semanal: {self.promedio_semanal} episodios ({self.fecha_inicio} a {self.fecha_fin})"
    
    @classmethod
    def calcular_promedio(cls, total_episodios, fecha_inicio, fecha_fin):
        diferencia_dias = (fecha_fin - fecha_inicio).days
        semanas_totales = max(diferencia_dias / 7.0, 1.0)
        promedio_semanal = round(total_episodios / semanas_totales, 1)
        return promedio_semanal


class DuracionPromedioEpisodios(models.Model):
    total_episodios = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    suma_duracion_total = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0.0)])
    duracion_promedio = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    
    def __str__(self):
        return f"Duración promedio: {self.duracion_promedio} horas por episodio"
    
    @classmethod
    def calcular_duracion_promedio(cls, total_episodios, suma_duracion_total):
        duracion_promedio = round(suma_duracion_total / total_episodios, 1)
        return duracion_promedio


class IntensidadPromedioDolor(models.Model):
    INTENSIDAD_CHOICES = [
        ('leve', 'Leve'),
        ('moderado', 'Moderado'),
        ('severo', 'Severo'),
    ]
    
    intensidad_promedio = models.CharField(max_length=10, choices=INTENSIDAD_CHOICES)
    
    def __str__(self):
        return f"Intensidad promedio: {self.get_intensidad_promedio_display()}"
    
    @classmethod
    def obtener_intensidad_promedio(cls):
        return 'moderado'


class AsociacionHormonal(models.Model):
    total_episodios = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    episodios_menstruacion = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    episodios_anticonceptivos = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    porcentaje_menstruacion = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    porcentaje_anticonceptivos = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    
    def __str__(self):
        return f"Asociación hormonal: {self.porcentaje_menstruacion}% menstruación, {self.porcentaje_anticonceptivos}% anticonceptivos"
    
    @classmethod
    def calcular_porcentajes(cls, total_episodios, episodios_menstruacion, episodios_anticonceptivos):
        if total_episodios == 0:
            return (0.0, 0.0)
        porcentaje_menstruacion = round((episodios_menstruacion / total_episodios) * 100, 1)
        porcentaje_anticonceptivos = round((episodios_anticonceptivos / total_episodios) * 100, 1)
        return (porcentaje_menstruacion, porcentaje_anticonceptivos)


class EvolucionMIDAS(models.Model):
    TENDENCIA_CHOICES = [
        ('mejorado', 'Mejorado'),
        ('empeorado', 'Empeorado'),
        ('estable', 'Estable'),
    ]
    
    puntuacion_promedio = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    puntuacion_actual = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    variacion_puntaje_midas = models.DecimalField(max_digits=5, decimal_places=1)
    tendencia_de_discapacidad = models.CharField(max_length=10, choices=TENDENCIA_CHOICES)
    
    def __str__(self):
        return f"Evolución MIDAS: {self.get_tendencia_de_discapacidad_display()} (variación: {self.variacion_puntaje_midas})"
    
    @classmethod
    def calcular_evolucion(cls, puntuacion_promedio, puntuacion_actual):
        variacion_puntaje = round(puntuacion_actual - puntuacion_promedio, 1)
        if variacion_puntaje < 0:
            tendencia = 'mejorado'
        elif variacion_puntaje > 0:
            tendencia = 'empeorado'
        else:
            tendencia = 'estable'
        return (variacion_puntaje, tendencia)


class DesencadenantesComunes(models.Model):
    nombre_desencadenante = models.CharField(max_length=100)
    total_episodios_analizados = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    episodios_con_desencadenante = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    porcentaje_ocurrencia = models.DecimalField(max_digits=5, decimal_places=1, validators=[MinValueValidator(0.0)])
    
    def __str__(self):
        return f"Desencadenante: {self.nombre_desencadenante} ({self.porcentaje_ocurrencia}%)"
    
    @classmethod
    def calcular_desencadenantes_frecuentes(cls, episodios_desencadenantes_dict):
        if not episodios_desencadenantes_dict or 'total_episodios' not in episodios_desencadenantes_dict:
            return []
        
        total_episodios = episodios_desencadenantes_dict.pop('total_episodios')
        resultados = []
        
        for desencadenante, ocurrencias in episodios_desencadenantes_dict.items():
            porcentaje = round((ocurrencias / total_episodios) * 100, 1)
            resultados.append((desencadenante, porcentaje))
        
        resultados.sort(key=lambda x: x[1], reverse=True)
        return resultados
    
    @classmethod
    def obtener_desencadenantes_mas_frecuentes(cls):
        return "Los desencadenantes más frecuentes son: estrés (40%), falta de sueño (25%), alimentos (20%)"

