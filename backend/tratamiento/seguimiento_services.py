from datetime import timezone


class SeguimientoService:
    """Servicio especializado en seguimiento de tratamientos"""

    UMBRAL_CUMPLIMIENTO_ALTO = 80.0
    UMBRAL_CUMPLIMIENTO_BAJO = 80.0

    def __init__(self, tratamiento_service):
        self._tratamiento_service = tratamiento_service

    def evaluar_cumplimiento(self, tratamiento_id):
        """Evalúa el cumplimiento actual del tratamiento"""
        estadisticas = self._tratamiento_service.obtener_estadisticas_cumplimiento(tratamiento_id)
        if not estadisticas:
            return None

        porcentaje = estadisticas['porcentaje_cumplimiento']
        return {
            'porcentaje': porcentaje,
            'categoria': self._categorizar_cumplimiento(porcentaje),
            'estadisticas': estadisticas
        }

    def decidir_accion_seguimiento(self, porcentaje_cumplimiento):
        """Decide qué acción tomar basada en el cumplimiento"""
        if porcentaje_cumplimiento >= self.UMBRAL_CUMPLIMIENTO_ALTO:
            return 'modificar'
        elif porcentaje_cumplimiento < self.UMBRAL_CUMPLIMIENTO_BAJO:
            return 'cancelar'
        else:
            return 'mantener'

    def generar_reporte_seguimiento(self, tratamiento_id):
        """Genera un reporte completo de seguimiento"""
        evaluacion = self.evaluar_cumplimiento(tratamiento_id)
        if not evaluacion:
            return None

        accion_recomendada = self.decidir_accion_seguimiento(evaluacion['porcentaje'])

        return {
            'tratamiento_id': tratamiento_id,
            'evaluacion': evaluacion,
            'accion_recomendada': accion_recomendada,
            'fecha_evaluacion': timezone.now(),
            'recomendaciones_adicionales': self._generar_recomendaciones_adicionales(evaluacion)
        }

    def _categorizar_cumplimiento(self, porcentaje):
        """Categoriza el nivel de cumplimiento"""
        if porcentaje >= self.UMBRAL_CUMPLIMIENTO_ALTO:
            return 'alto'
        else:
            return 'bajo'

    def _generar_recomendaciones_adicionales(self, evaluacion):
        """Genera recomendaciones adicionales basadas en la evaluación"""
        categoria = evaluacion['categoria']

        if categoria == 'bajo':
            return [
                "Revisar barreras para el cumplimiento",
                "Considerar simplificar el régimen",
                "Evaluar efectos secundarios"
            ]
        else:
            return [
                "Mantener el régimen actual",
                "Considerar optimizaciones menores"
            ]
