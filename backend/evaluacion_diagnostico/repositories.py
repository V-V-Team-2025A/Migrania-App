# evaluacion_diagnostico/repositories.py
import abc
from typing import List
from django.utils import timezone


class AbstractAutoevaluacionMidasRepository(abc.ABC):
    """
    Contrato base para repositorios de autoevaluaciones MIDAS.
    """

    @abc.abstractmethod
    def crear_autoevaluacion(self, paciente, fecha):
        """Crear nueva autoevaluación MIDAS"""
        raise NotImplementedError

    @abc.abstractmethod
    def obtener_autoevaluaciones(self, paciente) -> List:
        """Obtener todas las autoevaluaciones de un paciente"""
        raise NotImplementedError

    @abc.abstractmethod
    def obtener_ultima_autoevaluacion(self, paciente):
        """Obtener la última evaluación de un paciente"""
        raise NotImplementedError

    @abc.abstractmethod
    def agregar_respuesta(self, autoevaluacion, pregunta, valor_respuesta: int):
        """Agregar respuesta a una evaluación MIDAS"""
        raise NotImplementedError

    @abc.abstractmethod
    def finalizar(self, autoevaluacion):
        """Actualizar y guardar puntaje total"""
        raise NotImplementedError


class DjangoAutoevaluacionMidasRepository(AbstractAutoevaluacionMidasRepository):
    """
    Implementación del repositorio de autoevaluaciones MIDAS usando Django ORM.
    """

    def __init__(self):
        from .models import AutoevaluacionMidas, Respuesta
        self.autoevaluacion_midas = AutoevaluacionMidas
        self.respuesta = Respuesta

    def crear_autoevaluacion(self, paciente, fecha):
        """
        Crear una nueva autoevaluación MIDAS para un paciente.
        """
        autoevaluacion = self.autoevaluacion_midas.objects.create(paciente=paciente)
        return autoevaluacion

    def obtener_autoevaluaciones(self, paciente) -> List:
        """
        Obtener todas las autoevaluaciones de un paciente ordenadas por fecha.
        """
        return list(self.autoevaluacion_midas.objects.filter(paciente=paciente).order_by('-fecha_autoevaluacion'))

    def obtener_ultima_autoevaluacion(self, paciente):
        """
        Obtener la última autoevaluación MIDAS de un paciente.
        """
        try:
            return self.autoevaluacion_midas.objects.filter(paciente=paciente).latest('fecha_autoevaluacion')
        except self.autoevaluacion_midas.DoesNotExist:
            return None

    def agregar_respuesta(self, autoevaluacion, pregunta, valor_respuesta: int):
        """
        Agregar una respuesta a una pregunta de la autoevaluación MIDAS.
        """
        return self.respuesta.objects.create(
            autoevaluacion=autoevaluacion,
            pregunta=pregunta,
            valor_respuesta=valor_respuesta
        )

    def finalizar(self, autoevaluacion):
        autoevaluacion.actualizar_puntaje_total()
        return autoevaluacion


class FakeAutoevaluacionMidasRepository(AbstractAutoevaluacionMidasRepository):
    """
    Implementación falsa del repositorio de autoevaluaciones MIDAS para pruebas.
    """

    def __init__(self):
        self._autoevaluaciones = []
        self._next_id = 1
        self._models_loaded = False
        self.autoevaluacion_midas = None
        self.respuesta = None

    def _load_models(self):
        """Cargar modelos Django solo cuando se necesiten (lazy loading)"""
        if not self._models_loaded:
            from .models import AutoevaluacionMidas, Respuesta
            self.autoevaluacion_midas = AutoevaluacionMidas
            self.respuesta = Respuesta
            self._models_loaded = True

    def _get_next_id(self):
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def crear_autoevaluacion(self, paciente, fecha):
        self._load_models()
        autoevaluacion = self.autoevaluacion_midas(
            id=self._get_next_id(),
            paciente=paciente,
            fecha_autoevaluacion=fecha,
            puntaje_total=0
        )
        autoevaluacion.respuestas_midas_individuales.set([])
        self._autoevaluaciones.append(autoevaluacion)
        return autoevaluacion

    def obtener_autoevaluaciones(self, paciente) -> List:
        return sorted(
            [a for a in self._autoevaluaciones if a.paciente == paciente],
            key=lambda x: x.fecha_autoevaluacion,
            reverse=True
        )

    def obtener_ultima_autoevaluacion(self, paciente):
        autoevaluaciones = self.obtener_autoevaluaciones(paciente)
        return autoevaluaciones[0] if autoevaluaciones else None

    def agregar_respuesta(self, autoevaluacion, pregunta, valor_respuesta: int):
        self._load_models()
        if len(autoevaluacion.respuestas_midas_individuales) >= 5:
            raise ValueError("No se pueden agregar más de 5 respuestas.")
        respuesta = self.respuesta(
            autoevaluacion=autoevaluacion,
            pregunta=pregunta,
            valor_respuesta=valor_respuesta,
            respondido_en=timezone.now()
        )
        autoevaluacion.respuestas_midas_individuales.append(respuesta)
        return respuesta

    def finalizar(self, autoevaluacion):
        total = sum(r.valor_respuesta for r in autoevaluacion.respuestas_midas_individuales)
        autoevaluacion.puntaje_total = total
        return autoevaluacion

    def limpiar_repositorio(self):
        """Útil para resetear entre escenarios BDD"""
        self._autoevaluaciones.clear()
        self._next_id = 1

    def obtener_todas_autoevaluaciones(self) -> List:
        """Obtener todas las autoevaluaciones (útil para testing)"""
        return self._autoevaluaciones.copy()
