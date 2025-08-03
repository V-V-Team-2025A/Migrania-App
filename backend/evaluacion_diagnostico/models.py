# evaluacion_diagnostico/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from usuarios.models import Usuario


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
        help_text='¿El episodio ocurrió durante la menstruación?'
    )
    anticonceptivos = models.BooleanField(
        verbose_name='Uso de Anticonceptivos',
        help_text='¿La paciente usa anticonceptivos hormonales?'
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