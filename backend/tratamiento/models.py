from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from usuarios.models import PacienteProfile
from evaluacion_diagnostico.models import  EpisodioCefalea

class EstadoNotificacion(models.TextChoices):
    ACTIVO = 'activo'
    SIN_CONFIRMAR = 'sin_confirmar'
    CONFIRMADO_TOMADO = 'tomado'
    CONFIRMADO_NO_TOMADO = 'no_tomado'
    CONFIRMADO_TOMADO_TARDE = 'tomado_tarde'
    CONFIRMADO_TOMADO_MUY_TARDE = 'tomado_muy_tarde'

class Recomendacion(models.TextChoices):
    RUTINA_SUENO = "rutina_sueno", "Mantener una rutina regular de sueño"
    EJERCICIO_MODERADO = "ejercicio_moderado", "Realizar ejercicio de forma moderada"
    CONTROL_ESTRES = "control_estres", "Controlar los niveles de estrés"
    HIDRATACION = "hidratacion", "Mantener una hidratación adecuada"
    AMBIENTE_OSCURO = "ambiente_oscuro", "Buscar un ambiente oscuro y silencioso"
    COMPRESION = "compresion", "Aplicar compresión fría o tibia"
    EVITAR_ESFUERZO = "evitar_esfuerzo", "Evitar esfuerzo físico durante el episodio"
    NAUSEAS_VOMITOS = "nauseas_vomitos", "Líquidos en pequeñas cantidades y evitar alimentos pesados"

    # Exclusivas para mujeres
    MENSTRUACION = "menstruacion", "Usar analgésicos adecuados durante la menstruación"
    ANTICONCEPTIVOS = "anticonceptivos", "Consultar con un ginecólogo sobre anticonceptivos hormonales"

    def __str__(self):
        return f"{self.label} ({self.value})"

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    caracteristica = models.CharField(blank=True)
    hora_de_inicio = models.TimeField()
    frecuencia_horas = models.IntegerField(default=8)
    duracion_dias = models.IntegerField()

    def calcular_fechas_de_tomas(self, fecha_inicio=None):
        if fecha_inicio is None:
            fecha_inicio = datetime.today().date()
        fechas_tomas = []
        for dia in range(self.duracion_dias):
            fecha_actual = fecha_inicio + timedelta(days=dia)
            tomas_por_dia = 24 // self.frecuencia_horas
            for i in range(tomas_por_dia):
                hora_toma = datetime.combine(fecha_actual, self.hora_de_inicio) + timedelta(hours=i*self.frecuencia_horas)
                fechas_tomas.append(hora_toma)
        return sorted(fechas_tomas)

    def calcular_recordatorios(self, fechas_tomas):
        return [fecha_toma - timedelta(minutes=30) for fecha_toma in fechas_tomas]

    def __str__(self):
        return f"{self.nombre} {self.dosis} (cada {self.frecuencia_horas} horas)"

class Notificacion(models.Model):
    """Clase base para las notificaciones (abstracta)"""
    mensaje = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=30, choices=EstadoNotificacion.choices, default=EstadoNotificacion.ACTIVO)
    tratamiento = models.ForeignKey('Tratamiento', related_name='%(class)ss', on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True

    def obtener_estado(self):
        return self.estado

    def asignar_estado(self, estado):
        self.estado = estado

    def es_hora_de_envio(self, ahora):
        return ahora >= self.fecha_hora

class Alerta(Notificacion):
    """Modelo para alertas de toma de medicamentos"""
    numero_alerta = models.IntegerField()
    duracion = models.IntegerField()
    tiempo_espera = models.IntegerField()

    def enviar(self):
        if self.estado == EstadoNotificacion.ACTIVO:
            self.estado = EstadoNotificacion.SIN_CONFIRMAR
            return True
        return False

    def reenviar(self, ahora=None):
        if self.estado != EstadoNotificacion.SIN_CONFIRMAR:
            return None

        if ahora is None:
            ahora = timezone.now()

        siguiente_numero = self.numero_alerta + 1
        self.estado = EstadoNotificacion.CONFIRMADO_NO_TOMADO

        if siguiente_numero > 3:
            return None

        # Crear nueva alerta
        nueva_alerta = Alerta(
            mensaje=f"{self.mensaje.split(' (Alerta')[0]} (Alerta #{siguiente_numero})",
            fecha_hora=ahora,
            estado=EstadoNotificacion.ACTIVO,
            tratamiento=self.tratamiento,
            numero_alerta=siguiente_numero,
            duracion=self.duracion,
            tiempo_espera=self.tiempo_espera
        )
        return nueva_alerta

    def ha_excedido_hora_de_confirmacion(self, ahora=None):
        if ahora is None:
            ahora = timezone.now()
        tiempo_transcurrido = (ahora - self.fecha_hora).total_seconds() / 60
        return tiempo_transcurrido > self.duracion

    def confirmar_tomado(self, hora_confirmacion=None):
        if hora_confirmacion is None:
            hora_confirmacion = timezone.now()

        tiempo_transcurrido = (hora_confirmacion - self.fecha_hora).total_seconds() / 60

        if tiempo_transcurrido <= 15:
            self.estado = EstadoNotificacion.CONFIRMADO_TOMADO
        elif tiempo_transcurrido <= 30:
            self.estado = EstadoNotificacion.CONFIRMADO_TOMADO_TARDE
        else:
            self.estado = EstadoNotificacion.CONFIRMADO_TOMADO_MUY_TARDE

        return self.estado

    def confirmar_no_tomado(self):
        self.estado = EstadoNotificacion.CONFIRMADO_NO_TOMADO

    def __str__(self):
        return f"Alerta #{self.numero_alerta}: {self.mensaje} - {self.estado}"

class Recordatorio(Notificacion):
    """Modelo para recordatorios de medicamentos y recomendaciones"""
    def enviar(self):
        self.estado = EstadoNotificacion.ACTIVO
        return True

    def __str__(self):
        return f"Recordatorio: {self.mensaje} - {self.estado}"

class Tratamiento(models.Model):
    episodio = models.OneToOneField(
        EpisodioCefalea,
        on_delete=models.CASCADE,
        related_name='tratamiento',
        verbose_name='Episodio de Cefalea'
    )
    paciente = models.ForeignKey(
        PacienteProfile,
        on_delete=models.CASCADE,
        related_name='tratamientos',
        verbose_name='Paciente',
    )
    medicamentos = models.ManyToManyField(Medicamento)
    recomendaciones = models.JSONField(default=list)
    fecha_inicio = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    cumplimiento = models.FloatField(default=0.0)
    motivo_cancelacion = models.TextField(blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fecha_inicio and not kwargs.get('fecha_inicio'):
            self.fecha_inicio = datetime.now().date()

    @property
    def tipo_migraña(self):
        return self.episodio.categoria_diagnostica if self.episodio else "Sin episodio"

    @property
    def porcentaje_cumplimiento(self):
        return self.cumplimiento

    @property
    def porcentaje_cumplimiento(self):
        return self.cumplimiento

    def asignar_recomendaciones_generales(self):
        self.recomendaciones = [
            Recomendacion.RUTINA_SUENO,
            Recomendacion.EJERCICIO_MODERADO,
            Recomendacion.CONTROL_ESTRES,
            Recomendacion.HIDRATACION,
            Recomendacion.AMBIENTE_OSCURO,
            Recomendacion.COMPRESION,
            Recomendacion.EVITAR_ESFUERZO,
            Recomendacion.NAUSEAS_VOMITOS,
        ]


    def agregar_recomendaciones_para_mujer(self):
        self.recomendaciones.append(Recomendacion.MENSTRUACION)
        self.recomendaciones.append(Recomendacion.ANTICONCEPTIVOS)

    def generar_notificaciones(self, fecha_actual=None, repository=None):
        if fecha_actual is None:
            fecha_actual = timezone.now().date()
        if repository is None:
            raise ValueError("Se requiere un repositorio para generar notificaciones")

        todas_notificaciones = []

        medicamentos = repository.get_medicamentos_by_tratamiento_id(self.id)

        # Generar notificaciones de medicamentos
        for medicamento in medicamentos:
            notificaciones_med = self._generar_notificaciones_medicamento(medicamento, fecha_actual)
            todas_notificaciones.extend(notificaciones_med)

        # Generar notificaciones de recomendaciones
        for rec in self.recomendaciones:
            notificaciones_rec = self._generar_notificaciones_recomendacion(rec, fecha_actual, repository)
            todas_notificaciones.extend(notificaciones_rec)

        return todas_notificaciones

    def _generar_notificaciones_medicamento(self, medicamento, fecha_actual=None):
        if fecha_actual is None:
            fecha_actual = timezone.now().date()

        notificaciones = []

        # Calcular todas las fechas de tomas
        fechas_tomas = medicamento.calcular_fechas_de_tomas(self.fecha_inicio)
        fechas_recordatorios = medicamento.calcular_recordatorios(fechas_tomas)

        for fecha_recordatorio in fechas_recordatorios:
            # Solo generar recordatorios para la fecha actual o futura
            if fecha_recordatorio.date() >= fecha_actual:
                recordatorio = Recordatorio(
                    mensaje=f"Recordatorio: Debe tomar su medicación '{medicamento.nombre}' pronto",
                    fecha_hora=timezone.make_aware(fecha_recordatorio),
                    estado=EstadoNotificacion.ACTIVO,
                    tratamiento=self
                )
                notificaciones.append(recordatorio)

        return notificaciones

    def _generar_notificaciones_recomendacion(self, recomendacion, fecha_actual=None, repository=None):
        if fecha_actual is None:
            fecha_actual = timezone.now().date()

        notificaciones = []
        fecha_base = fecha_actual
        duracion = self.calcular_duracion(repository=repository)

        # Si no hay medicamentos, usar al menos 1 día de duración
        if duracion <= 0:
            duracion = 1

        for i in range(duracion):
            fecha = fecha_base + timedelta(days=i)
            hora_recomendacion = datetime.combine(fecha, datetime.min.time().replace(hour=9))

            # Asegurarnos de que la hora tenga timezone
            try:
                hora_recomendacion = timezone.make_aware(hora_recomendacion)
            except ValueError:
                # Ya tiene timezone
                pass

            recordatorio = Recordatorio(
                mensaje=f"Recordatorio de recomendación: {recomendacion}",
                fecha_hora=hora_recomendacion,
                estado=EstadoNotificacion.ACTIVO,
                tratamiento=self
            )
            notificaciones.append(recordatorio)

        return notificaciones

    def confirmar_toma(self, alerta_id, tomado=True):
        try:
            alerta = self.alertas.get(id=alerta_id)
            if tomado:
                return alerta.confirmar_tomado()
            else:
                return alerta.confirmar_no_tomado()
        except Alerta.DoesNotExist:
            return False

    def esta_activo(self, fecha_actual=None, repository=None):
        if not self.activo:
            return False
        duracion = self.calcular_duracion(repository=repository)
        if duracion > 0 and self.fecha_inicio:
            fecha_fin = self.fecha_inicio + timedelta(days=duracion)
            if fecha_actual is None:
                fecha_actual = timezone.now().date()
            return fecha_actual <= fecha_fin
        return True

    def procesar_notificaciones_pendientes(self, ahora=None):
        if ahora is None:
            ahora = timezone.now()

        if not self.esta_activo(ahora.date()):
            return []

        notificaciones_procesadas = []

        # Procesar alertas pendientes
        alertas_a_enviar = self.alertas.filter(
            estado=EstadoNotificacion.ACTIVO,
            fecha_hora__lte=ahora
        ).order_by('fecha_hora')

        for alerta in alertas_a_enviar:
            alerta.enviar()
            notificaciones_procesadas.append(alerta)

            # Si es una alerta sin confirmar y ha excedido el tiempo
            if (alerta.estado == EstadoNotificacion.SIN_CONFIRMAR and
                alerta.ha_excedido_hora_de_confirmacion(ahora)):

                # Crear la siguiente alerta si es necesario
                nueva_alerta = alerta.reenviar(ahora)
                if nueva_alerta:
                    # Verificar si ya es hora de enviar la nueva alerta
                    if nueva_alerta.es_hora_de_envio(ahora):
                        nueva_alerta.enviar()
                    notificaciones_procesadas.append(nueva_alerta)

        # Procesar recordatorios pendientes
        recordatorios_a_enviar = self.recordatorios.filter(
            estado=EstadoNotificacion.ACTIVO,
            fecha_hora__lte=ahora
        ).order_by('fecha_hora')

        for recordatorio in recordatorios_a_enviar:
            recordatorio.enviar()
            notificaciones_procesadas.append(recordatorio)

        return notificaciones_procesadas

    def calcular_cumplimiento(self):
        alertas_tratamiento = Alerta.objects.filter(id__in=self.notificaciones_generadas        )

        if not alertas_tratamiento.exists():
            return 0.0

        total_alertas = alertas_tratamiento.count()

        # Estados que consideramos como "cumplimiento positivo"
        estados_cumplimiento = [
            EstadoNotificacion.CONFIRMADO_TOMADO,
            EstadoNotificacion.CONFIRMADO_TOMADO_TARDE,
            EstadoNotificacion.CONFIRMADO_TOMADO_MUY_TARDE
        ]

        # Contar alertas confirmadas como tomadas (en cualquier momento)
        alertas_cumplidas = alertas_tratamiento.filter(estado__in=estados_cumplimiento).count()

        # Calcular porcentaje
        porcentaje_cumplimiento = (alertas_cumplidas / total_alertas) * 100

        # Actualizar el campo cumplimiento del modelo
        self.cumplimiento = round(porcentaje_cumplimiento, 2)
        self.save(update_fields=['cumplimiento'])

        return self.cumplimiento

    def calcular_duracion(self, repository=None):
        medicamentos = repository.get_medicamentos_by_tratamiento_id(self.id)
        if not medicamentos:
            return 0
        return max([med.duracion_dias for med in medicamentos])

    def __str__(self):
        if self.pk:  # Verificar si la instancia tiene un ID asignado
            return f"Tratamiento {self.id} - Medicamentos: {self.medicamentos.count()}"
        return "Tratamiento sin inicializar"