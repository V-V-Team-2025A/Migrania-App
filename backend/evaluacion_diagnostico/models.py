# evaluacion_diagnostico/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from usuarios.models import Usuario
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

class EpisodioCefalea(models.Model):
    """
    Modelo para registrar episodios de cefalea del paciente.

    Permite el registro detallado de características de episodios de cefalea
    para facilitar el diagnóstico médico y seguimiento del paciente.
    Incluye categorización automática basada en criterios médicos estándar.
    """

    # Constantes para choices
    SEVERIDAD_CHOICES = [
        ('Leve', 'Leve'),
        ('Moderada', 'Moderada'),
        ('Severa', 'Severa'),
    ]

    LOCALIZACION_CHOICES = [
        ('Unilateral', 'Unilateral'),
        ('Bilateral', 'Bilateral'),
    ]

    CARACTER_DOLOR_CHOICES = [
        ('Pulsátil', 'Pulsátil'),
        ('Opresivo', 'Opresivo'),
        ('Punzante', 'Punzante'),
    ]

    SINTOMAS_AURA_CHOICES = [
        ('Visuales', 'Visuales'),
        ('Sensitivos', 'Sensitivos'),
        ('De habla o lenguaje', 'De habla o lenguaje'),
        ('Motores', 'Motores'),
        ('Troncoencefálicos', 'Troncoencefálicos'),
        ('Retinianos', 'Retinianos'),
        ('Ninguno', 'Ninguno'),
    ]

    CATEGORIA_CEFALEA_CHOICES = [
        ('Migraña sin aura', 'Migraña sin aura'),
        ('Migraña con aura', 'Migraña con aura'),
        ('Cefalea de tipo tensional', 'Cefalea de tipo tensional'),
    ]

    # Relaciones
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='episodios_cefalea',
        limit_choices_to={'tipo_usuario': Usuario.TipoUsuario.PACIENTE},
        verbose_name='Paciente'
    )

    # Características principales del episodio
    duracion_cefalea_horas = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(72)],
        verbose_name='Duración Cefalea (horas)',
        help_text='Duración del episodio en horas (1-72)'
    )
    severidad = models.CharField(
        max_length=20,
        choices=SEVERIDAD_CHOICES,
        verbose_name='Severidad del Dolor'
    )
    localizacion = models.CharField(
        max_length=20,
        choices=LOCALIZACION_CHOICES,
        verbose_name='Localización del Dolor'
    )
    caracter_dolor = models.CharField(
        max_length=20,
        choices=CARACTER_DOLOR_CHOICES,
        verbose_name='Carácter del Dolor'
    )

    # Síntomas asociados
    empeora_actividad = models.BooleanField(
        verbose_name='Empeora con Actividad',
        help_text='¿El dolor empeora con actividad física?'
    )
    nauseas_vomitos = models.BooleanField(
        verbose_name='Náuseas o Vómitos'
    )
    fotofobia = models.BooleanField(
        verbose_name='Sensibilidad a la Luz'
    )
    fonofobia = models.BooleanField(
        verbose_name='Sensibilidad al Sonido'
    )

    # Datos del aura
    presencia_aura = models.BooleanField(
        verbose_name='Presencia de Aura'
    )
    sintomas_aura = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Síntomas del Aura',
        help_text='Síntomas de aura separados por comas. Ej: Visuales, Sensitivos'
    )
    duracion_aura_minutos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        verbose_name='Duración del Aura (min)',
        help_text='Duración del aura en minutos (0-120)'
    )

    # Datos específicos para mujeres
    en_menstruacion = models.BooleanField(
        verbose_name='En menstruación',
        help_text='¿El episodio ocurrió durante la menstruación?',
        default=False
    )
    anticonceptivos = models.BooleanField(
        verbose_name='Uso de Anticonceptivos',
        help_text='¿La paciente usa anticonceptivos hormonales?',
        default=False

    )

    # Categorización diagnóstica
    categoria_diagnostica = models.CharField(
        max_length=50,
        choices=CATEGORIA_CEFALEA_CHOICES,
        blank=True,
        verbose_name='Categoría Diagnóstica',
        help_text='Categorización automática basada en criterios médicos'
    )

    # Auditoría - Solo fecha de creación según convenciones
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )

    class Meta:
        verbose_name = 'Episodio de Cefalea'
        verbose_name_plural = 'Episodios de Cefalea'
        db_table = 'evaluacion_episodio_cefalea'
        ordering = ['-creado_en']
        indexes = [
            models.Index(fields=['paciente']),
            models.Index(fields=['categoria_diagnostica']),
            models.Index(fields=['creado_en']),
            models.Index(fields=['severidad']),
        ]

    def __str__(self):
        """Representación string del episodio"""
        fecha_str = self.creado_en.strftime('%d/%m/%Y') if self.creado_en else 'Sin fecha'
        categoria = self.categoria_diagnostica or 'Sin categorizar'
        return f"{self.paciente.get_full_name()} - {categoria} ({fecha_str})"

    def clean(self):
        """
        Validaciones de integridad a nivel de modelo.
        """
        super().clean()

        # Validar coherencia de datos de aura
        if self.presencia_aura and self.duracion_aura_minutos == 0:
            raise ValidationError({
                'duracion_aura_minutos': 'Si hay presencia de aura, la duración debe ser mayor a 0.'
            })

        if not self.presencia_aura and self.duracion_aura_minutos > 0:
            raise ValidationError({
                'duracion_aura_minutos': 'Si no hay aura, la duración debe ser 0.'
            })

    @property
    def sintomas_aura_list(self):
        """
        Convierte string de síntomas a lista para facilitar procesamiento
        
        Returns:
            list: Lista de síntomas de aura
        """
        if not self.sintomas_aura or self.sintomas_aura.lower() == 'ninguno':
            return []
        return [s.strip() for s in self.sintomas_aura.split(',') if s.strip()]