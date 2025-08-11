# tratamiento/tratamiento_service.py
from datetime import datetime, timedelta
from django.utils import timezone
from tratamiento.models import Tratamiento, Recordatorio, Alerta, EstadoNotificacion


class TratamientoService:
    def __init__(self, repository):
        self.tratamiento_repository = repository

    def crear_tratamiento(self, paciente, episodio=None, recomendaciones=None, fecha_inicio=None, activo=True):
        # Validaciones
        errores = self._validar_datos_tratamiento(paciente, episodio, recomendaciones, fecha_inicio)
        if errores:
            raise ValueError(f"Datos de tratamiento inválidos: {', '.join(errores)}")

        tratamiento_existente = Tratamiento.objects.filter(episodio=episodio).first()
        if tratamiento_existente:
            # Asegura que el repo conozca el tratamiento existente
            self.tratamiento_repository.save_tratamiento(tratamiento_existente)
            return tratamiento_existente

        tratamiento = Tratamiento(
            paciente=paciente,
            episodio=episodio,
            fecha_inicio=fecha_inicio,
            activo=activo
        )
        tratamiento.save()

        # Sincroniza con el repo fake siempre
        self.tratamiento_repository.save_tratamiento(tratamiento)

        if recomendaciones:
            # JSONField -> asignar lista y guardar
            tratamiento.recomendaciones = list(recomendaciones)
            tratamiento.save(update_fields=["recomendaciones"])

        return tratamiento

    def _validar_datos_tratamiento(self, paciente, episodio, recomendaciones, fecha_inicio):
        """Validar datos del tratamiento según reglas de negocio"""
        errores = []

        # Validar paciente
        if not paciente:
            errores.append("El paciente es obligatorio")

        # Validar episodio (puede ser opcional dependiendo del caso de uso)
        if episodio is None:
            # Podría ser válido en algunos casos, pero agregar advertencia
            pass

        # Validar fecha de inicio
        if fecha_inicio and fecha_inicio > datetime.now().date():
            errores.append("La fecha de inicio no puede ser futura")

        return errores

    def modificar_tratamiento(self, tratamiento_id, nuevos_datos):
        """Modifica un tratamiento existente"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            raise ValueError(f"Tratamiento con ID {tratamiento_id} no encontrado")

        # Aplicar modificaciones
        for campo, valor in nuevos_datos.items():
            if hasattr(tratamiento, campo):
                setattr(tratamiento, campo, valor)

        return self.tratamiento_repository.save_tratamiento(tratamiento)

    def cancelar_tratamiento(self, tratamiento_id, motivo):
        """Cancela un tratamiento con el motivo especificado"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            raise ValueError(f"Tratamiento con ID {tratamiento_id} no encontrado")

        tratamiento.cancelar(motivo)
        return self.tratamiento_repository.save_tratamiento(tratamiento)

    def agregar_medicamento_a_tratamiento(self, tratamiento_id, medicamento):
        """Agregar un medicamento al tratamiento"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return False

        # Si el medicamento no existe, lo guardamos primero
        if not getattr(medicamento, "id", None):
            medicamento = self.tratamiento_repository.save_medicamento(medicamento)

        return self.tratamiento_repository.add_medicamento_to_tratamiento(tratamiento_id, medicamento.id)

    def obtener_estadisticas_cumplimiento(self, tratamiento_id):
        """Obtiene estadísticas detalladas de cumplimiento"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return None

        return {
            'porcentaje_cumplimiento': tratamiento.cumplimiento,
            'estaActivo': tratamiento.esta_activo(),
            'duracion_dias': tratamiento.calcular_duracion(),
            'fecha_inicio': tratamiento.fecha_inicio,
            'total_medicamentos': tratamiento.medicamentos.count() if hasattr(tratamiento.medicamentos, 'count') else 0
        }

    def generar_notificaciones(self, tratamiento_id, dias_anticipacion=7):
        """Generar notificaciones para un tratamiento (por días de anticipación)"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return []

        notificaciones = tratamiento.generarNotificaciones(dias_anticipacion=dias_anticipacion)
        for notificacion in notificaciones:
            if isinstance(notificacion, Recordatorio):
                self.tratamiento_repository.save_recordatorio(notificacion)
            elif isinstance(notificacion, Alerta):
                self.tratamiento_repository.save_alerta(notificacion)

        return notificaciones

    def procesar_notificaciones_pendientes(self, tratamiento_id):
        """Procesar notificaciones pendientes"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return []

        notificaciones_procesadas = tratamiento.procesarNotificacionesPendientes()

        # Guardar las notificaciones procesadas
        for notificacion in notificaciones_procesadas:
            if isinstance(notificacion, Recordatorio):
                self.tratamiento_repository.save_recordatorio(notificacion)
            elif isinstance(notificacion, Alerta):
                self.tratamiento_repository.save_alerta(notificacion)

        return notificaciones_procesadas

    def confirmar_toma(self, alerta_id, tomado=True, hora_confirmacion=None):
        """Confirmar la toma de un medicamento"""
        if hora_confirmacion is None:
            hora_confirmacion = timezone.now()

        alerta = self.tratamiento_repository.get_alerta_by_id(alerta_id)
        if not alerta:
            return None

        if tomado:
            estado = alerta.confirmarTomado(hora_confirmacion)
        else:
            estado = alerta.confirmarNoTomado()

        self.tratamiento_repository.save_alerta(alerta)
        return estado

    def obtener_proxima_notificacion(self, tratamiento_id):
        """Obtener la próxima notificación a enviar"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return None

        return tratamiento.obtenerSiguienteNotificacion()

    def generar_recordatorio_recomendacion(self, tratamiento_id, recomendacion, hora_actual=None):
        """Generar un recordatorio de recomendación específico"""
        if hora_actual is None:
            hora_actual = timezone.now()

        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return None

        recordatorio = Recordatorio(
            mensaje=f"Recordatorio de recomendación: {recomendacion}",
            fecha_hora=hora_actual,
            estado=EstadoNotificacion.ACTIVO
        )
        self.tratamiento_repository.save_recordatorio(recordatorio)
        return recordatorio
