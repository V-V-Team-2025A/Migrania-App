from django.db import models
from collections import deque
from datetime import datetime, timedelta
import logging
import re

logger = logging.getLogger(__name__)

class EstadoNotificacion(models.TextChoices):
    ACTIVO = 'activo'
    SIN_CONFIRMAR = 'sin_confirmar'
    CONFIRMADO_TOMADO = 'tomado'
    CONFIRMADO_NO_TOMADO = 'no_tomado'
    CONFIRMADO_TOMADO_TARDE = 'tomado_tarde'
    CONFIRMADO_TOMADO_MUY_TARDE = 'tomado_muy_tarde'

class Recomendacion(models.TextChoices):
    HIDRATACION = 'hidratacion'
    EJERCICIO_SUAVE = 'ejercicio_suave'
    DIARIO_DE_DOLOR = 'diario_de_dolor'
    MEDITACION = 'meditacion'

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

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=11, unique=True)
    tratamiento = models.ForeignKey('Tratamiento', on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if not re.match(r'^\d{10}$', self.identificacion):
            raise ValueError("La identificación debe ser una cédula ecuatoriana válida (10 dígitos numéricos)")

    def asignarTratamiento(self, tratamiento):
        self.tratamiento = tratamiento
        self.save()

    def estaTratamientoActivo(self):
        return self.tratamiento is not None and self.tratamiento.estaActivo()

    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    dosis = models.CharField(max_length=50)
    hora_de_inicio = models.TimeField()
    frecuencia = models.IntegerField(default=8)
    duracion_dias = models.IntegerField()

    def calcularFechasDeTomas(self, fecha_inicio=None):
        if fecha_inicio is None:
            fecha_inicio = datetime.today().date()

        inicio = datetime.combine(fecha_inicio, self.hora_de_inicio)

        fechas_tomas = []
        for dia in range(self.duracion_dias):
            fecha_actual = fecha_inicio + timedelta(days=dia)

            tomas_por_dia = 24 // self.frecuencia

            for i in range(tomas_por_dia):
                hora_toma = datetime.combine(fecha_actual, self.hora_de_inicio) + timedelta(hours=i*self.frecuencia)
                fechas_tomas.append(hora_toma)

        return sorted(fechas_tomas)

    def calcularRecordatorios(self, fechas_tomas):
        return [fecha_toma - timedelta(minutes=30) for fecha_toma in fechas_tomas]

    def __str__(self):
        return f"{self.nombre} {self.dosis} (cada {self.frecuencia} horas)"

class Tratamiento(models.Model):
    medicamentos = models.ManyToManyField(Medicamento)
    recomendaciones = models.JSONField(default=list)
    fecha_inicio = models.DateField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bicola_notificacion = BicolaNotificacion()
        if not self.fecha_inicio and not kwargs.get('fecha_inicio'):
            self.fecha_inicio = datetime.now().date()

    def generarNotificaciones(self, dias_anticipacion=7):
        todas_notificaciones = []
        fecha_limite = None

        if dias_anticipacion > 0:
            fecha_limite = datetime.now() + timedelta(days=dias_anticipacion)

        for medicamento in self.medicamentos.all():
            notificaciones_med = self._generar_notificaciones_medicamento(
                medicamento, fecha_limite
            )
            todas_notificaciones.extend(notificaciones_med)

        for rec in self.recomendaciones:
            notificaciones_rec = self._generar_notificaciones_recomendacion(
                rec, dias_anticipacion, fecha_limite
            )
            todas_notificaciones.extend(notificaciones_rec)

        if todas_notificaciones:
            self.bicola_notificacion.agregar_multiples(todas_notificaciones)

        logger.info(f"Generadas {len(todas_notificaciones)} notificaciones para el tratamiento")
        return todas_notificaciones

    def _generar_notificaciones_medicamento(self, medicamento, fecha_limite=None):
        notificaciones = []

        fechas_tomas = medicamento.calcularFechasDeTomas(self.fecha_inicio)

        if fecha_limite:
            fechas_tomas = [fecha for fecha in fechas_tomas if fecha <= fecha_limite]

        fechas_recordatorios = medicamento.calcularRecordatorios(fechas_tomas)

        for i, fecha_recordatorio in enumerate(fechas_recordatorios):
            recordatorio = Recordatorio(
                mensaje=f"Recordatorio para tomar {medicamento.nombre} ({medicamento.dosis})",
                fecha_hora=fecha_recordatorio,
                estado=EstadoNotificacion.ACTIVO
            )
            recordatorio.save()
            notificaciones.append(recordatorio)

        for i, fecha_toma in enumerate(fechas_tomas):
            alerta = Alerta(
                mensaje=f"Es hora de tomar {medicamento.nombre} ({medicamento.dosis})",
                fecha_hora=fecha_toma,
                estado=EstadoNotificacion.ACTIVO,
                numero_alerta=1,
                duracion=15,
                tiempo_espera=15
            )
            alerta.save()
            notificaciones.append(alerta)

        logger.info(f"Generadas {len(notificaciones)} notificaciones para medicamento {medicamento.nombre}")
        return notificaciones

    def _generar_notificaciones_recomendacion(self, recomendacion, dias=7, fecha_limite=None):
        notificaciones = []
        fecha_base = datetime.now().date()

        if fecha_limite:
            dias_hasta_limite = (fecha_limite.date() - fecha_base).days + 1
            dias = min(dias, dias_hasta_limite)

        for i in range(dias):
            fecha = fecha_base + timedelta(days=i)
            hora_recomendacion = datetime.combine(fecha, datetime.min.time().replace(hour=9))

            recordatorio = Recordatorio(
                mensaje=f"Recordatorio de recomendación: {recomendacion}",
                fecha_hora=hora_recomendacion,
                estado=EstadoNotificacion.ACTIVO
            )
            recordatorio.save()
            notificaciones.append(recordatorio)

        logger.info(f"Generadas {len(notificaciones)} notificaciones para recomendación {recomendacion}")
        return notificaciones

    def confirmarToma(self, notificacion, estado):
        if not isinstance(notificacion, Alerta):
            logger.warning(f"Se intentó confirmar una notificación que no es alerta: {notificacion}")
            return False

        notificacion.estado = estado
        notificacion.save()
        return True

    def calcularDuracion(self):
        if self.medicamentos.exists():
            return max(m.duracion_dias for m in self.medicamentos.all())
        return 0

    def estaActivo(self):
        if not self.activo:
            return False

        duracion = self.calcularDuracion()
        if duracion > 0 and self.fecha_inicio:
            fecha_fin = self.fecha_inicio + timedelta(days=duracion)
            return datetime.now().date() <= fecha_fin

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

    def __str__(self):
        return f"Tratamiento {self.id} - Medicamentos: {self.medicamentos.count()}"

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
