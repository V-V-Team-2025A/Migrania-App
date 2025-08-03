# evaluacion_diagnostico/models.py
from django.core.exceptions import ValidationError
from django.db import models
import numpy as np

from migraine_app import settings

PUNTAJE_MAX_POR_PREGUNTA = 90
PUNTAJE_MIN_POR_PREGUNTA = 0


class PreguntaMidas(models.Model):
    """
    Pregunta de la evaluación MIDAS.
    Contiene las preguntas de la evaluación, similar a una enumeración.
    """
    texto_pregunta = models.TextField(verbose_name='Texto de la Pregunta')
    orden_pregunta = models.PositiveIntegerField(unique=True, verbose_name='Orden de la Pregunta')
    # AUDITORÍA
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'evaluacion_diagnostico_pregunta_midas'
        ordering = ['orden_pregunta']
        verbose_name = 'Pregunta MIDAS'
        verbose_name_plural = 'Preguntas MIDAS'

    def __str__(self):
        return f"Pregunta N.{self.orden_pregunta}: {self.texto_pregunta}"


class EvaluacionMidas(models.Model):
    """
    Evaluación MIDAS de un usuario.
    Contiene la fecha en que se realizó la evaluación y el puntaje total.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # TODO revisar si es correcto este enlace
        on_delete=models.CASCADE,
        related_name='evaluaciones_midas',
        verbose_name='Usuario'
    )
    fecha_evaluacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Evaluación')
    puntaje_total = models.PositiveIntegerField(default=0, verbose_name='Puntaje Total')

    class Meta:
        db_table = 'evaluacion_diagnostico_evaluacion_midas'
        ordering = ['-fecha_evaluacion']  # mas reciente primero
        verbose_name = 'Evaluación MIDAS'
        verbose_name_plural = 'Evaluaciones MIDAS'
        indexes = [
            models.Index(fields=['usuario', 'fecha_evaluacion'])
        ]

    def puede_realizar_nueva_evaluacion(self):
        """
        Validación para asegurar que el usuario puede realizar una nueva evaluación
        luego de 3 meses de la última evaluación.
        """
        ultima_evaluacion = EvaluacionMidas.objects.filter(usuario=self.usuario).order_by(
            '-fecha_evaluacion').first()

        if not ultima_evaluacion:
            # Si no hay evaluaciones previas, puede realizar una nueva
            return True

        fecha_ultima_evaluacion = np.datetime64(ultima_evaluacion.fecha_evaluacion.date(), 'M')
        fecha_actual = np.datetime64(self.fecha_evaluacion.date(), 'M')
        fecha_luego_de_tres_meses = fecha_ultima_evaluacion + np.timedelta64(3, 'M')

        return fecha_actual == fecha_luego_de_tres_meses

    def save(self, *args, **kwargs):
        self.full_clean()  # validar todos los campos antes de guardar
        super().save(*args, **kwargs)
        # Calcular puntaje_total después de guardar
        if not self.puntaje_total:
            self.calcular_puntaje_total()

    def calcular_puntaje_total(self):
        """
        Calcula el puntaje total de la evaluación
        """
        total = self.respuestas_midas_individuales.aggregate(total=models.Sum('valor_respuesta'))['total'] or 0
        self.puntaje_total = total
        self.save(update_fields=['puntaje_total'])

    def __str__(self):
        return f"Evaluación MIDAS de {self.usuario.nombre_completo} - {self.fecha_evaluacion.date()}"


class RespuestaMidas(models.Model):
    """
    Respuesta a una pregunta de la evaluación MIDAS
    """
    evaluacion = models.ForeignKey(
        EvaluacionMidas,
        on_delete=models.CASCADE,
        related_name='respuestas_midas_individuales',
        verbose_name='Evaluación MIDAS'
    )
    pregunta = models.ForeignKey(
        PreguntaMidas,
        on_delete=models.CASCADE,
        related_name='respuesta_a_pregunta',
        verbose_name='Pregunta'
    )
    valor_respuesta = models.PositiveIntegerField(verbose_name='Valor de la Pregunta')
    respondido_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'evaluacion_diagnostico_respuesta_midas'
        unique_together = ('evaluacion', 'pregunta')  # una respuesta por pregunta en una evaluación
        verbose_name = 'Respuesta MIDAS'
        verbose_name_plural = 'Respuestas MIDAS'

    def clean(self):
        """
        Validaciones personalizadas para la respuesta
        """
        if self.pregunta is None:
            raise ValidationError("La pregunta no puede ser nula")
        if not (PUNTAJE_MIN_POR_PREGUNTA <= self.valor_respuesta <= PUNTAJE_MAX_POR_PREGUNTA):
            raise ValidationError(
                f"El valor de respuesta debe estar entre {PUNTAJE_MIN_POR_PREGUNTA} y {PUNTAJE_MAX_POR_PREGUNTA}.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.evaluacion.calcular_puntaje_total()

    def __str__(self):
        return f"Pregunta {self.pregunta.orden_pregunta} - {self.pregunta.texto_pregunta} \n Respuesta: {self.valor_respuesta}"
