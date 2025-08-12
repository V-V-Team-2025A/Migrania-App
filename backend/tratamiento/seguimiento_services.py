from django.utils import timezone
from tratamiento.constants import UMBRAL_CUMPLIMIENTO_ALTO, UMBRAL_CUMPLIMIENTO_BAJO

class SeguimientoService:
    UMBRAL_CUMPLIMIENTO_ALTO = UMBRAL_CUMPLIMIENTO_ALTO
    UMBRAL_CUMPLIMIENTO_BAJO = UMBRAL_CUMPLIMIENTO_BAJO

    def __init__(self, tratamiento_service):
        self._tratamiento_service = tratamiento_service

    def evaluar_cumplimiento(self, tratamiento_id):
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
        if porcentaje_cumplimiento >= self.UMBRAL_CUMPLIMIENTO_ALTO:
            return 'modificar'
        elif porcentaje_cumplimiento <= self.UMBRAL_CUMPLIMIENTO_BAJO:
            return 'cancelar'
        else:
            return 'mantener'

    def generar_reporte_seguimiento(self, tratamiento_id):
        evaluacion = self.evaluar_cumplimiento(tratamiento_id)
        if not evaluacion:
            return None
        return {
            'tratamiento_id': tratamiento_id,
            'evaluacion': evaluacion,
            'accion_recomendada': self.decidir_accion_seguimiento(evaluacion['porcentaje']),
            'fecha_evaluacion': timezone.now(),
            'recomendaciones_adicionales': self._generar_recomendaciones_adicionales(evaluacion)
        }

    def _categorizar_cumplimiento(self, porcentaje):
        return 'alto' if porcentaje >= self.UMBRAL_CUMPLIMIENTO_ALTO else 'bajo'

    def _generar_recomendaciones_adicionales(self, evaluacion):
        if evaluacion['categoria'] == 'bajo':
            return [
                "Revisar barreras para el cumplimiento",
                "Considerar simplificar el régimen",
                "Evaluar efectos secundarios",
            ]
        return ["Mantener el régimen actual", "Considerar optimizaciones menores"]
