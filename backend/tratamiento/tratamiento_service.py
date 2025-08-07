from datetime import datetime, timedelta
from django.utils import timezone
from tratamiento.models import Medicamento, Tratamiento, Recordatorio, Alerta, EstadoNotificacion


class TratamientoService:
    def __init__(self, repository):
        self.tratamiento_repository = repository

    def crear_medicamento(self, nombre, dosis, caracteristica, hora_inicio, frecuencia_horas, duracion_dias):
        """Crear un nuevo medicamento"""
        medicamento = Medicamento(
            nombre=nombre,
            dosis=dosis,
            caracteristica=caracteristica,
            hora_de_inicio=hora_inicio,
            frecuencia_horas=frecuencia_horas,
            duracion_dias=duracion_dias
        )
        return self.tratamiento_repository.save_medicamento(medicamento)

    def crear_tratamiento(self, paciente, episodio=None, recomendaciones=None, fecha_inicio=None, activo=True):
        tratamiento_existente = Tratamiento.objects.filter(episodio=episodio).first()
        if tratamiento_existente:
            return tratamiento_existente

        tratamiento = Tratamiento(
            paciente=paciente,
            episodio=episodio,
            fecha_inicio=fecha_inicio,
            activo=activo
        )
        tratamiento.save()

        if recomendaciones:
            tratamiento.recomendaciones.set(recomendaciones)

        return tratamiento

    def agregar_medicamento_a_tratamiento(self, tratamiento_id, medicamento):
        """Agregar un medicamento al tratamiento"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return False

        # Si el medicamento no existe, lo guardamos primero
        if not medicamento.id:
            medicamento = self.tratamiento_repository.save_medicamento(medicamento)

        return self.tratamiento_repository.add_medicamento_to_tratamiento(tratamiento_id, medicamento.id)

    def generar_notificaciones(self, tratamiento_id, fecha_actual=None):
        """Generar notificaciones para un tratamiento"""
        if fecha_actual is None:
            fecha_actual = timezone.now().date()

        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return []

        notificaciones = tratamiento.generarNotificaciones(fecha_actual)
        for notificacion in notificaciones:
            if isinstance(notificacion, Recordatorio):
                self.tratamiento_repository.save_recordatorio(notificacion)
            elif isinstance(notificacion, Alerta):
                self.tratamiento_repository.save_alerta(notificacion)

        return notificaciones

    def procesar_notificaciones_pendientes(self, tratamiento_id, ahora=None):
        """Procesar notificaciones pendientes"""
        if ahora is None:
            ahora = timezone.now()

        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return []

        notificaciones_procesadas = tratamiento.procesarNotificacionesPendientes(ahora)

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

    def obtener_proxima_notificacion(self, tratamiento_id, ahora=None):
        """Obtener la próxima notificación a enviar"""
        if ahora is None:
            ahora = timezone.now()

        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return None

        return tratamiento.obtenerSiguienteNotificacion(ahora)

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
            estado=EstadoNotificacion.ACTIVO,
            tratamiento=tratamiento
        )

        return self.tratamiento_repository.save_recordatorio(recordatorio)
