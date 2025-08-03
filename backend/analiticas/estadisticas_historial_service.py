from typing import Dict, List, Tuple, Any, Optional
from datetime import date
from django.core.exceptions import ValidationError
from .repositories import AbstractEstadisticaHistorialRepository, DjangoEstadisticaHistorialRepository


class EstadisticaHistorialService:
    
    def __init__(self, repository: AbstractEstadisticaHistorialRepository = None):
        self.repository = repository or DjangoEstadisticaHistorialRepository()
    
    def analizar_promedio_semanal(self, total_episodios: int, fecha_inicio: date, fecha_fin: date) -> Dict[str, Any]:
        try:
            if total_episodios < 0:
                raise ValidationError("El número de episodios no puede ser negativo")
            
            if fecha_inicio > fecha_fin:
                raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin")
            
            promedio = self.repository.calcular_promedio_semanal(total_episodios, fecha_inicio, fecha_fin)
            
            return {
                'promedio_semanal': promedio,
                'total_episodios': total_episodios,
                'periodo_analizado': {
                    'inicio': fecha_inicio,
                    'fin': fecha_fin
                },
                'interpretacion': self._interpretar_promedio_semanal(promedio)
            }
        except Exception as e:
            raise ValidationError(f"Error al calcular promedio semanal: {str(e)}")
    
    def analizar_duracion_promedio(self, total_episodios: int, suma_duracion_total: float) -> Dict[str, Any]:
        try:
            if total_episodios <= 0:
                raise ValidationError("El número de episodios debe ser mayor a cero")
            
            if suma_duracion_total < 0:
                raise ValidationError("La duración total no puede ser negativa")
            
            duracion_promedio = self.repository.calcular_duracion_promedio(total_episodios, suma_duracion_total)
            
            return {
                'duracion_promedio': duracion_promedio,
                'total_episodios': total_episodios,
                'suma_duracion_total': suma_duracion_total,
                'interpretacion': self._interpretar_duracion_promedio(duracion_promedio)
            }
        except Exception as e:
            raise ValidationError(f"Error al calcular duración promedio: {str(e)}")
    
    def analizar_intensidad_promedio(self, intensidades: Optional[List[int]] = None) -> Dict[str, Any]:
        try:
            if intensidades:
                for intensidad in intensidades:
                    if not 1 <= intensidad <= 10:
                        raise ValidationError("Las intensidades deben estar entre 1 y 10")
            
            intensidad_promedio = self.repository.calcular_intensidad_promedio(intensidades)
            
            return {
                'intensidad_promedio': intensidad_promedio,
                'total_registros': len(intensidades) if intensidades else 0,
                'interpretacion': self._interpretar_intensidad_promedio(intensidad_promedio)
            }
        except Exception as e:
            raise ValidationError(f"Error al calcular intensidad promedio: {str(e)}")
    
    def analizar_asociacion_hormonal(self, total_episodios: int, episodios_menstruacion: int, 
                                   episodios_anticonceptivos: int) -> Dict[str, Any]:
        try:
            if total_episodios <= 0:
                raise ValidationError("El número total de episodios debe ser mayor a cero")
            
            if episodios_menstruacion < 0 or episodios_anticonceptivos < 0:
                raise ValidationError("Los números de episodios no pueden ser negativos")
            
            if episodios_menstruacion > total_episodios or episodios_anticonceptivos > total_episodios:
                raise ValidationError("Los episodios específicos no pueden exceder el total")
            
            porcentajes = self.repository.calcular_asociacion_hormonal(
                total_episodios, episodios_menstruacion, episodios_anticonceptivos
            )
            
            return {
                'porcentaje_menstruacion': porcentajes[0],
                'porcentaje_anticonceptivos': porcentajes[1],
                'total_episodios': total_episodios,
                'interpretacion': self._interpretar_asociacion_hormonal(porcentajes[0], porcentajes[1])
            }
        except Exception as e:
            raise ValidationError(f"Error al calcular asociación hormonal: {str(e)}")
    
    def analizar_evolucion_midas(self, puntuacion_promedio: float, puntuacion_actual: float) -> Dict[str, Any]:
        try:
            if puntuacion_promedio < 0 or puntuacion_actual < 0:
                raise ValidationError("Las puntuaciones MIDAS no pueden ser negativas")
            
            evolucion = self.repository.calcular_evolucion_midas(puntuacion_promedio, puntuacion_actual)
            
            return {
                'variacion_puntaje': evolucion[0],
                'tendencia_discapacidad': evolucion[1],
                'puntuacion_promedio': puntuacion_promedio,
                'puntuacion_actual': puntuacion_actual,
                'interpretacion': self._interpretar_evolucion_midas(evolucion[1], evolucion[0])
            }
        except Exception as e:
            raise ValidationError(f"Error al calcular evolución MIDAS: {str(e)}")
    
    def analizar_desencadenantes_comunes(self, desencadenantes_dict: Dict[str, int]) -> Dict[str, Any]:
        try:
            if not desencadenantes_dict:
                raise ValidationError("Debe proporcionar al menos un desencadenante")
            
            for desencadenante, frecuencia in desencadenantes_dict.items():
                if frecuencia < 0:
                    raise ValidationError(f"La frecuencia de '{desencadenante}' no puede ser negativa")
            
            resultado = self.repository.calcular_desencadenantes_comunes(desencadenantes_dict)
            
            return {
                'desencadenantes_ordenados': resultado,
                'total_desencadenantes': len(desencadenantes_dict),
                'interpretacion': self._interpretar_desencadenantes_comunes(resultado)
            }
        except Exception as e:
            raise ValidationError(f"Error al calcular desencadenantes comunes: {str(e)}")
    
    def generar_reporte_completo(self, datos_estadisticas: Dict[str, Any]) -> Dict[str, Any]:
        reporte = {
            'resumen_ejecutivo': {},
            'analisis_detallado': {},
            'recomendaciones': []
        }
        
        try:
            if all(key in datos_estadisticas for key in ['total_episodios', 'fecha_inicio', 'fecha_fin']):
                reporte['analisis_detallado']['promedio_semanal'] = self.analizar_promedio_semanal(
                    datos_estadisticas['total_episodios'],
                    datos_estadisticas['fecha_inicio'],
                    datos_estadisticas['fecha_fin']
                )
            
            if all(key in datos_estadisticas for key in ['total_episodios', 'suma_duracion_total']):
                reporte['analisis_detallado']['duracion_promedio'] = self.analizar_duracion_promedio(
                    datos_estadisticas['total_episodios'],
                    datos_estadisticas['suma_duracion_total']
                )
            
            if 'intensidades' in datos_estadisticas:
                reporte['analisis_detallado']['intensidad_promedio'] = self.analizar_intensidad_promedio(
                    datos_estadisticas['intensidades']
                )
            
            if all(key in datos_estadisticas for key in ['total_episodios', 'episodios_menstruacion', 'episodios_anticonceptivos']):
                reporte['analisis_detallado']['asociacion_hormonal'] = self.analizar_asociacion_hormonal(
                    datos_estadisticas['total_episodios'],
                    datos_estadisticas['episodios_menstruacion'],
                    datos_estadisticas['episodios_anticonceptivos']
                )
            
            if all(key in datos_estadisticas for key in ['puntuacion_promedio', 'puntuacion_actual']):
                reporte['analisis_detallado']['evolucion_midas'] = self.analizar_evolucion_midas(
                    datos_estadisticas['puntuacion_promedio'],
                    datos_estadisticas['puntuacion_actual']
                )
            
            if 'desencadenantes_dict' in datos_estadisticas:
                reporte['analisis_detallado']['desencadenantes_comunes'] = self.analizar_desencadenantes_comunes(
                    datos_estadisticas['desencadenantes_dict']
                )
            
            reporte['resumen_ejecutivo'] = self._generar_resumen_ejecutivo(reporte['analisis_detallado'])
            reporte['recomendaciones'] = self._generar_recomendaciones(reporte['analisis_detallado'])
            
            return reporte
            
        except Exception as e:
            raise ValidationError(f"Error al generar reporte completo: {str(e)}")
    
    def _interpretar_promedio_semanal(self, promedio: float) -> str:
        if promedio <= 1:
            return "Frecuencia baja de episodios"
        elif promedio <= 3:
            return "Frecuencia moderada de episodios"
        else:
            return "Frecuencia alta de episodios"
    
    def _interpretar_duracion_promedio(self, duracion: float) -> str:
        if duracion <= 4:
            return "Episodios de duración corta"
        elif duracion <= 12:
            return "Episodios de duración moderada"
        else:
            return "Episodios de duración prolongada"
    
    def _interpretar_intensidad_promedio(self, intensidad: str) -> str:
        interpretaciones = {
            'leve': "Dolor de intensidad manejable",
            'moderado': "Dolor de intensidad considerable",
            'severo': "Dolor de intensidad alta, requiere atención"
        }
        return interpretaciones.get(intensidad.lower(), "Intensidad no definida")
    
    def _interpretar_asociacion_hormonal(self, porcentaje_menstruacion: float, porcentaje_anticonceptivos: float) -> str:
        if porcentaje_menstruacion > 50:
            return "Fuerte asociación con ciclo menstrual"
        elif porcentaje_anticonceptivos > 30:
            return "Posible asociación con anticonceptivos"
        else:
            return "Asociación hormonal limitada"
    
    def _interpretar_evolucion_midas(self, tendencia: str, variacion: float) -> str:
        if tendencia == "mejorado":
            return f"Mejora significativa en discapacidad ({abs(variacion)} puntos menos)"
        elif tendencia == "empeorado":
            return f"Aumento en discapacidad ({variacion} puntos más)"
        else:
            return "Discapacidad estable sin cambios significativos"
    
    def _interpretar_desencadenantes_comunes(self, desencadenantes: List[Tuple[str, float]]) -> str:
        if not desencadenantes:
            return "No se identificaron desencadenantes principales"
        
        principal = desencadenantes[0]
        return f"Principal desencadenante: {principal[0]} ({principal[1]:.1f}% de los casos)"
    
    def _generar_resumen_ejecutivo(self, analisis: Dict[str, Any]) -> Dict[str, str]:
        resumen = {}
        
        if 'promedio_semanal' in analisis:
            promedio = analisis['promedio_semanal']['promedio_semanal']
            resumen['frecuencia'] = f"Promedio de {promedio:.1f} episodios por semana"
        
        if 'duracion_promedio' in analisis:
            duracion = analisis['duracion_promedio']['duracion_promedio']
            resumen['duracion'] = f"Duración promedio de {duracion:.1f} horas por episodio"
        
        if 'intensidad_promedio' in analisis:
            intensidad = analisis['intensidad_promedio']['intensidad_promedio']
            resumen['intensidad'] = f"Intensidad promedio: {intensidad}"
        
        return resumen
    
    def _generar_recomendaciones(self, analisis: Dict[str, Any]) -> List[str]:
        recomendaciones = []
        
        if 'promedio_semanal' in analisis:
            promedio = analisis['promedio_semanal']['promedio_semanal']
            if promedio > 3:
                recomendaciones.append("Considerar consulta médica por alta frecuencia de episodios")
        
        if 'duracion_promedio' in analisis:
            duracion = analisis['duracion_promedio']['duracion_promedio']
            if duracion > 12:
                recomendaciones.append("Evaluar tratamientos para reducir duración de episodios")
        
        if 'asociacion_hormonal' in analisis:
            porcentaje_menst = analisis['asociacion_hormonal']['porcentaje_menstruacion']
            if porcentaje_menst > 50:
                recomendaciones.append("Considerar tratamiento hormonal preventivo")
        
        return recomendaciones
