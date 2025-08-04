# evaluacion_diagnostico/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError

from usuarios.models import Usuario
from django.core.exceptions import ValidationError

class AutoevaluacionMidas(models.Model):
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='autoevaluaciones_midas',
                                 limit_choices_to={'tipo_usuario': Usuario.TipoUsuario.PACIENTE},
                                 verbose_name='Paciente')
    fecha_autoevaluacion = models.DateField(auto_now_add=True, verbose_name='Fecha de la autoevaluación')
    puntaje_total = models.PositiveIntegerField(default=0, verbose_name='Puntaje Total',
                                                help_text='Puntaje total de la autoevaluación MIDAS')

    GRADO_DISCAPACIDAD_CHOICES = [
        ('mínima', 'Grado I - Discapacidad mínima'),
        ('leve', 'Grado II - Discapacidad leve'),
        ('moderada', 'Grado III - Discapacidad moderada'),
        ('severa', 'Grado IV - Discapacidad severa'),
    ]

    grado_discapacidad = models.CharField(
        max_length=10,
        choices=GRADO_DISCAPACIDAD_CHOICES,
        blank=True,
        verbose_name='Grado de Discapacidad'
    )

    class Meta:
        db_table = 'evaluacion_midas'
        ordering = ['-fecha_autoevaluacion']
        unique_together = ('paciente', 'fecha_autoevaluacion')
        verbose_name = 'Evaluación MIDAS'
        verbose_name_plural = 'Evaluaciones MIDAS'
        indexes = [
            models.Index(fields=['paciente', 'fecha_autoevaluacion'])
        ]

    def __str__(self):
        return f"{self.paciente.nombre_completo} - {self.fecha_autoevaluacion}"

    def calcular_puntaje_total(self):
        """
        Calcula el puntaje total de la autoevaluación MIDAS sumando los valores de las respuestas.
        Si no hay respuestas, retorna 0.
        """
        return self.respuestas_midas_individuales.aggregate(
            total=models.Sum('valor_respuesta')
        )['total'] or 0

    def actualizar_puntaje_total(self):
        """
        Actualiza el puntaje total de la autoevaluación MIDAS.
        Llama al método calcular_puntaje_total y guarda el resultado en el campo puntaje_total.
        """
        self.puntaje_total = self.calcular_puntaje_total()
        self.grado_discapacidad = self.calcular_grado_discapacidad()
        self.save(update_fields=['puntaje_total', 'grado_discapacidad'])

    def calcular_grado_discapacidad(self):
        puntaje = self.calcular_puntaje_total()

        if puntaje <= 5:
            return 'mínima'
        elif puntaje <= 10:
            return 'leve'
        elif puntaje <= 20:
            return 'moderada'
        else:
            return 'severa'


class Pregunta(models.Model):
    """
    Modelo para registrar las preguntas de la autoevaluación MIDAS.

    Contiene las preguntas de la evaluación, similar a una enumeración.
    """
    enunciado_pregunta = models.TextField(verbose_name='Enunciado de la Pregunta')
    orden_pregunta = models.PositiveIntegerField(unique=True, verbose_name='Orden de la Pregunta')

    # Auditoría - Solo fecha de creación según convenciones
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'evaluacion_pregunta'
        ordering = ['orden_pregunta']
        verbose_name = 'Pregunta de la autoevaluacion MIDAS'
        verbose_name_plural = 'Preguntas de la autoevaluacion MIDAS'

    def __str__(self):
        """
        Representación en string de la pregunta.
        """
        return f"Pregunta N.{self.orden_pregunta}: {self.enunciado_pregunta}"


class Respuesta(models.Model):
    """
    Modelo para registrar las respuestas a las preguntas de la evaluación MIDAS.
    Cada respuesta está asociada a una evaluación MIDAS y una pregunta específica.
    Permite registrar el valor de la respuesta y la fecha en que fue respondida.
    """
    autoevaluacion = models.ForeignKey(
        AutoevaluacionMidas,
        on_delete=models.CASCADE,
        related_name='respuestas_midas_individuales',
        verbose_name='Evaluación MIDAS'
    )

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuesta_a_pregunta',
        verbose_name='Pregunta'
    )

    valor_respuesta = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)],
                                                       verbose_name='Valor de la Pregunta',
                                                       help_text='Número de días, debe estar entre 0 y 90.')

    # Auditoria - Fecha en que se respondió la pregunta
    respondido_en = models.DateTimeField(auto_now=True, verbose_name='Fecha de Respuesta')

    class Meta:
        db_table = 'evaluacion_respuesta'
        unique_together = ('autoevaluacion', 'pregunta')  # una respuesta por pregunta en una evaluación
        verbose_name = 'Respuesta MIDAS'
        verbose_name_plural = 'Respuestas MIDAS'

    def __str__(self):
        return (f"Pregunta {self.pregunta.orden_pregunta} - {self.pregunta.enunciado_pregunta} \n "
                f"Respuesta: {self.valor_respuesta}")
