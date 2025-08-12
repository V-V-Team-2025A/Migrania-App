from datetime import datetime
from django.utils import timezone
from tratamiento.models import Tratamiento, Recordatorio, Alerta, EstadoNotificacion


class TratamientoService:
    def __init__(self, repository):
        self.tratamiento_repository = repository

    # Creación y mantenimiento
    def crear_tratamiento(self, paciente, episodio=None, recomendaciones=None, fecha_inicio=None, activo=True):
        errores = self._validar_datos_tratamiento(paciente, episodio, recomendaciones, fecha_inicio)
        if errores:
            raise ValueError(f"Datos de tratamiento inválidos: {', '.join(errores)}")

        existing = (
            self.tratamiento_repository.get_tratamiento_by_episodio(episodio)
            if hasattr(self.tratamiento_repository, "get_tratamiento_by_episodio")
            else Tratamiento.objects.filter(episodio=episodio).first()
        )
        if existing:
            self.tratamiento_repository.save_tratamiento(existing)
            return existing

        tratamiento = Tratamiento(
            paciente=paciente, episodio=episodio, fecha_inicio=fecha_inicio, activo=activo
        )
        tratamiento.save()
        self.tratamiento_repository.save_tratamiento(tratamiento)

        if recomendaciones:
            tratamiento.recomendaciones = list(recomendaciones)
            tratamiento.save(update_fields=["recomendaciones"])

        return tratamiento

    def _validar_datos_tratamiento(self, paciente, episodio, recomendaciones, fecha_inicio):
        # Validar datos del tratamiento según reglas de negocio
        errores = []

        if not paciente:
            errores.append("El paciente es obligatorio")

        if fecha_inicio and fecha_inicio > datetime.now().date():
            errores.append("La fecha de inicio no puede ser futura")

        return errores

    def modificar_tratamiento(self, tratamiento_id, nuevos_datos):
        # Modifica un tratamiento existente
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            raise ValueError(f"Tratamiento con ID {tratamiento_id} no encontrado")

        for campo, valor in nuevos_datos.items():
            if hasattr(tratamiento, campo):
                setattr(tratamiento, campo, valor)

        return self.tratamiento_repository.save_tratamiento(tratamiento)

    def cancelar_tratamiento(self, tratamiento_id, motivo):
        # Cancela tratamiento con motivo
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            raise ValueError(f"Tratamiento con ID {tratamiento_id} no encontrado")

        tratamiento.cancelar(motivo)
        return self.tratamiento_repository.save_tratamiento(tratamiento)

    # Medicamentos
    def agregar_medicamento_a_tratamiento(self, tratamiento_id, medicamento):
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return False

        if not getattr(medicamento, "id", None):
            medicamento = self.tratamiento_repository.save_medicamento(medicamento)

        return self.tratamiento_repository.add_medicamento_to_tratamiento(tratamiento_id, medicamento.id)

    # Notificaciones y seguimiento
    def obtener_estadisticas_cumplimiento(self, tratamiento_id):
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return None

        return {
            'porcentaje_cumplimiento': tratamiento.cumplimiento,
            'esta_activo': tratamiento.esta_activo(),
            'duracion_dias': tratamiento.calcular_duracion(),
            'fecha_inicio': tratamiento.fecha_inicio,
            'total_medicamentos': tratamiento.medicamentos.count() if hasattr(tratamiento.medicamentos, 'count') else 0
        }

    def generar_notificaciones(self, tratamiento_id, dias_anticipacion=7):
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return []

        notificaciones = tratamiento.generar_notificaciones(dias_anticipacion=dias_anticipacion)
        for n in notificaciones:
            if isinstance(n, Recordatorio):
                self.tratamiento_repository.save_recordatorio(n)
            elif isinstance(n, Alerta):
                self.tratamiento_repository.save_alerta(n)

        return notificaciones

    def procesar_notificaciones_pendientes(self, tratamiento_id):
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return []

        notificaciones_procesadas = tratamiento.procesar_notificaciones_pendientes()

        for n in notificaciones_procesadas:
            if isinstance(n, Recordatorio):
                self.tratamiento_repository.save_recordatorio(n)
            elif isinstance(n, Alerta):
                self.tratamiento_repository.save_alerta(n)

        return notificaciones_procesadas

    def confirmar_toma(self, alerta_id, tomado=True, hora_confirmacion=None):
        #Confirmar la toma de un medicamento
        if hora_confirmacion is None:
            hora_confirmacion = timezone.now()

        alerta = self.tratamiento_repository.get_alerta_by_id(alerta_id)
        if not alerta:
            return None

        if tomado:
            delta_min = (hora_confirmacion - alerta.fecha_hora).total_seconds() / 60.0
            if delta_min <= alerta.duracion:
                estado = EstadoNotificacion.CONFIRMADO_TOMADO
            elif delta_min <= (alerta.duracion + alerta.tiempo_espera):
                estado = EstadoNotificacion.CONFIRMADO_TOMADO_TARDE
            else:
                estado = EstadoNotificacion.CONFIRMADO_TOMADO_MUY_TARDE
        else:
            estado = EstadoNotificacion.CONFIRMADO_NO_TOMADO  # <-- aquí estaba el typo

        alerta.estado = estado
        self.tratamiento_repository.save_alerta(alerta)
        return estado

    def obtener_proxima_notificacion(self, tratamiento_id):
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return None
        return tratamiento.obtener_siguiente_notificacion()

    def generar_recordatorio_recomendacion(self, tratamiento_id, recomendacion, hora_actual=None):
        # Genera un recordatorio de recomendación
        if hora_actual is None:
            hora_actual = timezone.now()

        recordatorio = Recordatorio(
            mensaje=f"Recordatorio de recomendación: {recomendacion}",
            fecha_hora=hora_actual,
            estado=EstadoNotificacion.ACTIVO
        )
        self.tratamiento_repository.save_recordatorio(recordatorio)
        return recordatorio
