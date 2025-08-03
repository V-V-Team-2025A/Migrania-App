from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from collections import deque
from datetime import datetime, timedelta
import logging


logger = logging.getLogger(__name__)


class EstadoNotificacion(models.TextChoices):
    ACTIVO = 'activo'
    SIN_CONFIRMAR = 'sin_confirmar'
    CONFIRMADO_TOMADO = 'tomado'
    CONFIRMADO_NO_TOMADO = 'no_tomado'
    CONFIRMADO_TOMADO_TARDE = 'tomado_tarde'
    CONFIRMADO_TOMADO_MUY_TARDE = 'tomado_muy_tarde'

    class BicolaNotificacion:
        def __init__(self):
            self.elementos = deque()

        def agregarFrente(self, elemento):
            self.elementos.appendleft(elemento)

        def agregarFinal(self, elemento):
            self.elementos.append(elemento)
            self.ordenar()

        def eliminarFrente(self):
            if self.elementos:
                return self.elementos.popleft()
            return None

        def eliminarFinal(self):
            if self.elementos:
                return self.elementos.pop()
            return None

        def verFrente(self):
            return self.elementos[0] if self.elementos else None

        def verFinal(self):
            return self.elementos[-1] if self.elementos else None

        def estaVacia(self):
            return len(self.elementos) == 0

        def ordenar(self):
            alertas_frente = []
            while (len(self.elementos) > 0 and
                   isinstance(self.elementos[0], Alerta) and
                   self.elementos[0].numero_alerta > 1):
                alertas_frente.append(self.elementos.popleft())

            self.elementos = deque(sorted(self.elementos, key=lambda n: n.fecha_hora))

            for alerta in reversed(alertas_frente):
                self.elementos.appendleft(alerta)

        def agregar_multiples(self, elementos):
            self.elementos.extend(elementos)
            self.ordenar()

        def __len__(self):
            return len(self.elementos)

        def listar_elementos(self):
            return list(self.elementos)


class Notificacion(models.Model):
    mensaje = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField()
    estado = models.CharField(max_length=30, choices=EstadoNotificacion.choices, default=EstadoNotificacion.ACTIVO)

    class Meta:
        abstract = True

    def enviar(self):
        raise NotImplementedError("Las subclases deben implementar este método")

    def obtenerEstado(self):
        return self.estado

    def asignarEstado(self, estado):
        self.estado = estado
        self.save()

    def esHoraDeEnvio(self, ahora):
        return ahora >= self.fecha_hora

    def actualizarEstadoSegunTiempo(self, ahora):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}: {self.mensaje} - {self.estado}"


class Alerta(Notificacion):
    numero_alerta = models.IntegerField()
    duracion = models.IntegerField()
    tiempo_espera = models.IntegerField()

    def enviar(self):
        if self.estado == EstadoNotificacion.ACTIVO:
            self.estado = EstadoNotificacion.SIN_CONFIRMAR
            self.save()
            logger.info(f"Alerta enviada: {self.mensaje} - Número: {self.numero_alerta}")
            return True
        return False

    def reenviar(self, bicola):
        siguiente_numero = self.numero_alerta + 1

        if siguiente_numero > 3:
            self.estado = EstadoNotificacion.CONFIRMADO_NO_TOMADO
            self.save()
            logger.info(f"Máximo de alertas alcanzado. Marcando como no tomado: {self.mensaje}")
            return None

        nueva_alerta = Alerta(
            mensaje=f"{self.mensaje} (Alerta #{siguiente_numero})",
            fecha_hora=datetime.now(),
            estado=EstadoNotificacion.ACTIVO,
            numero_alerta=siguiente_numero,
            duracion=self.duracion,
            tiempo_espera=self.tiempo_espera
        )
        nueva_alerta.save()

        bicola.agregarFrente(nueva_alerta)
        logger.info(f"Nueva alerta generada: {nueva_alerta.mensaje} - Número: {nueva_alerta.numero_alerta}")
        return nueva_alerta

    def haExcedidoHoraDeConfirmacion(self):
        ahora = datetime.now()
        tiempo_transcurrido = (ahora - self.fecha_hora).total_seconds() / 60
        return tiempo_transcurrido > self.duracion

    def actualizarEstadoSegunTiempo(self, ahora):
        if self.estado == EstadoNotificacion.ACTIVO:
            self.estado = EstadoNotificacion.SIN_CONFIRMAR
            self.save()

        tiempo_transcurrido = (ahora - self.fecha_hora).total_seconds() / 60

        if tiempo_transcurrido > self.duracion and self.estado == EstadoNotificacion.SIN_CONFIRMAR:
            return True

        return False


class Recordatorio(Notificacion):
    def enviar(self):
        logger.info(f"Recordatorio enviado: {self.mensaje}")
        return True

    def actualizarEstadoSegunTiempo(self, ahora):
        return False


class Recomendacion(models.Model):
    GENERO_CHOICES = [
        ('both', 'Hombre y Mujer'),
        ('female', 'Mujer'),
        ('male', 'Hombre'),
    ]

    clave = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    aplicable_a = models.CharField(max_length=6, choices=GENERO_CHOICES, default='both')

    @classmethod
    def obtener_por_genero(cls, genero_paciente):
        """
        Obtiene las recomendaciones aplicables según el género del paciente.

        Args:
            genero_paciente: 'male', 'female', o None

        Returns:
            QuerySet de recomendaciones aplicables
        """
        if genero_paciente == 'male':
            return cls.objects.filter(aplicable_a__in=['both', 'male'])
        elif genero_paciente == 'female':
            return cls.objects.filter(aplicable_a__in=['both', 'female'])
        else:
            # Si no se especifica género, devolver solo las generales
            return cls.objects.filter(aplicable_a='both')

    class Meta:
        verbose_name = 'Recomendación'
        verbose_name_plural = 'Recomendaciones'

    def __str__(self):
        return f"{self.descripcion} ({self.get_aplicable_a_display()})"


class Medicacion(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.CharField(max_length=50)
    caracteristica = models.TextField(blank=True)
    frecuencia = models.IntegerField(default=8)  # cada cuántas horas
    duracion = models.IntegerField()  # en días
    hora_de_inicio = models.TimeField()

    def calcularFechasDeTomas(self, fecha_inicio=None):
        if fecha_inicio is None:
            fecha_inicio = datetime.today().date()

        fechas_tomas = []
        for dia in range(self.duracion):
            fecha_actual = fecha_inicio + timedelta(days=dia)
            tomas_por_dia = 24 // self.frecuencia
            for i in range(tomas_por_dia):
                hora_toma = datetime.combine(fecha_actual, self.hora_de_inicio) + timedelta(
                    hours=i * self.frecuencia)
                fechas_tomas.append(hora_toma)

        return sorted(fechas_tomas)

    def calcularRecordatorios(self, fechas_tomas):
        return [fecha_toma - timedelta(minutes=30) for fecha_toma in fechas_tomas]

    def __str__(self):
        return f"{self.nombre} ({self.cantidad})"

    class Meta:
        verbose_name = 'Medicación'
        verbose_name_plural = 'Medicaciones'
        db_table = 'Medicacion'


class Tratamiento(models.Model):
    """Tratamiento médico prescrito por un médico para un paciente."""
    medico = models.ForeignKey('usuarios.MedicoProfile', on_delete=models.CASCADE)
    paciente = models.ForeignKey('usuarios.PacienteProfile', on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)

    medicaciones = models.ManyToManyField('Medicacion', blank=True, related_name='tratamientos')
    recomendaciones = models.ManyToManyField('Recomendacion', blank=True, related_name='tratamientos')

    activo = models.BooleanField(default=True)
    cumplimiento = models.FloatField(default=0.0)
    motivo_cancelacion = models.TextField(blank=True, null=True)

    notificaciones_generadas = JSONField(default=list, blank=True)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.id_tratamiento = None

    def _get_bicola(self):
        if not hasattr(self, '_bicola_notificacion'):
            # usa la clase ya definida en EstadoNotificacion
            self._bicola_notificacion = EstadoNotificacion.BicolaNotificacion()
        return self._bicola_notificacion

    @property
    def bicola_notificacion(self):
        return self._get_bicola()

    def agregar_medicacion(self, medicacion):
        """Asocia una medicación existente al tratamiento y la guarda."""
        medicacion.tratamiento = self
        medicacion.save()

    def agregar_recomendacion(self, recomendacion):
        """Asocia una recomendación existente al tratamiento y la guarda."""
        recomendacion.tratamiento = self
        recomendacion.save()

    def cancelar_tratamiento(self, motivo):
        """Cancela el tratamiento y registra el motivo."""
        self.activo = False
        self.motivo_cancelacion = motivo
        self.save()

    def modificar_tratamiento(self, nuevas_medicaciones, nuevas_recomendaciones):
        """Reemplaza las medicaciones y recomendaciones actuales."""
        self.medicaciones.clear()
        self.recomendaciones.clear()
        for m in nuevas_medicaciones:
            self.agregar_medicacion(m)
        for r in nuevas_recomendaciones:
            self.agregar_recomendacion(r)

    def generarNotificaciones(self, dias_anticipacion=7):
        todas_notificaciones = []
        fecha_limite = None

        if dias_anticipacion > 0:
            fecha_limite = datetime.now() + timedelta(days=dias_anticipacion)

        for medicacion in self.medicaciones.all():
            fechas_tomas = medicacion.calcularFechasDeTomas(self.fecha_inicio)
            if fecha_limite:
                fechas_tomas = [f for f in fechas_tomas if f <= fecha_limite]

            recordatorios = medicacion.calcularRecordatorios(fechas_tomas)

            for fr in recordatorios:
                r = Recordatorio(
                    mensaje=f"Recordatorio para tomar {medicacion.nombre} ({medicacion.cantidad})",
                    fecha_hora=fr,
                    estado=EstadoNotificacion.ACTIVO
                )
                r.save()
                todas_notificaciones.append(r)

            for ft in fechas_tomas:
                a = Alerta(
                    mensaje=f"Es hora de tomar {medicacion.nombre} ({medicacion.cantidad})",
                    fecha_hora=ft,
                    estado=EstadoNotificacion.ACTIVO,
                    numero_alerta=1,
                    duracion=15,
                    tiempo_espera=15
                )
                a.save()
                todas_notificaciones.append(a)

        for rec in self.recomendaciones.all():
            for i in range(dias_anticipacion):
                fecha = timezone.now().date() + timedelta(days=i)
                hora = datetime.combine(fecha, datetime.min.time().replace(hour=9))
                r = Recordatorio(
                    mensaje=f"Recordatorio de recomendación: {rec.descripcion}",
                    fecha_hora=hora,
                    estado=EstadoNotificacion.ACTIVO
                )
                r.save()
                todas_notificaciones.append(r)

        logger.info(f"Generadas {len(todas_notificaciones)} notificaciones para el tratamiento.")
        return todas_notificaciones

    def confirmarToma(self, notificacion, estado):
        if not isinstance(notificacion, Alerta):
            logger.warning("Notificación no válida")
            return False
        notificacion.estado = estado
        notificacion.save()
        # actualizar cumplimiento al confirmar
        self.actualizar_cumplimiento()
        return True

    def calcularDuracion(self):
        if self.medicaciones.exists():
            return max(m.duracion for m in self.medicaciones.all())
        return 0

    def estaActivo(self):
        if not self.activo:
            return False
        duracion = self.calcularDuracion()
        if duracion > 0 and self.fecha_inicio:
            fecha_fin = self.fecha_inicio + timedelta(days=duracion)
            return timezone.now().date() <= fecha_fin
        return True

    def obtenerSiguienteNotificacion(self):
        return self.bicola_notificacion.verFrente()

    def obtenerNotificacionesPendientes(self):
        return self.bicola_notificacion.listar_elementos()

    def procesarNotificacionesPendientes(self):
        if not self.estaActivo():
            logger.info(f"No se procesaron notificaciones porque el tratamiento no está activo")
            return []

        ahora = datetime.now()
        notificaciones_procesadas = []

        while not self.bicola_notificacion.estaVacia():
            notificacion = self.bicola_notificacion.verFrente()
            if notificacion.esHoraDeEnvio(ahora):
                notificacion_actual = self.bicola_notificacion.eliminarFrente()
                notificaciones_procesadas.append(notificacion_actual)

                notificacion_actual.enviar()

                if (isinstance(notificacion_actual, Alerta) and
                        notificacion_actual.estado == EstadoNotificacion.SIN_CONFIRMAR and
                        notificacion_actual.haExcedidoHoraDeConfirmacion()):
                    notificacion_actual.reenviar(self.bicola_notificacion)
            else:
                break

        return notificaciones_procesadas

    def actualizar_cumplimiento(self):
        # Estados que se consideran como tomados (incluye tardíos)
        estados_confirmados = {
            EstadoNotificacion.CONFIRMADO_TOMADO,
            EstadoNotificacion.CONFIRMADO_TOMADO_TARDE,
            EstadoNotificacion.CONFIRMADO_TOMADO_MUY_TARDE,
        }

        # Traer alertas entre las notificaciones que este tratamiento generó
        alertas = Alerta.objects.filter(pk__in=self.notificaciones_generadas)

        if not alertas.exists():
            self.cumplimiento = 0.0
            self.save()
            return self.cumplimiento

        total = alertas.count()
        confirmadas = alertas.filter(estado__in=estados_confirmados).count()

        cumplimiento = (confirmadas / total) * 100
        self.cumplimiento = round(cumplimiento, 2)
        self.save()
        return self.cumplimiento

    def __str__(self):
        return f"Tratamiento de {self.paciente} indicado por {self.medico} el {self.fecha_inicio}"

    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'
        db_table = 'tratamiento'
