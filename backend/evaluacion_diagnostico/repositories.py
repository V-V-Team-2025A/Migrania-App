# evaluacion_diagnostico/repositories.py
import abc
from typing import List, Dict, Any, Optional
from django.utils import timezone


class AbstractEpisodioCefaleaRepository(abc.ABC):
    """
    Contrato base para repositorios de episodios de cefalea.
    """

    @abc.abstractmethod
    def crear_episodio(self, paciente, datos_episodio: Dict[str, Any]):
        """Crear un nuevo episodio de cefalea"""
        raise NotImplementedError

    @abc.abstractmethod
    def obtener_episodios_paciente(self, paciente) -> List:
        """Obtener todos los episodios de un paciente"""
        raise NotImplementedError

    @abc.abstractmethod
    def obtener_episodio_por_id(self, episodio_id: int):
        """Obtener episodio por ID"""
        raise NotImplementedError

    @abc.abstractmethod
    def obtener_ultimo_episodio(self, paciente):
        """Obtener el último episodio de un paciente"""
        raise NotImplementedError

    @abc.abstractmethod
    def contar_episodios_paciente(self, paciente) -> int:
        """Contar episodios de un paciente"""
        raise NotImplementedError


class DjangoEpisodioCefaleaRepository(AbstractEpisodioCefaleaRepository):
    """
    Repositorio real usando Django ORM.
    """

    def __init__(self):
        from .models import EpisodioCefalea
        self.EpisodioCefalea = EpisodioCefalea

    def crear_episodio(self, paciente, datos_episodio: Dict[str, Any]):
        """Crear episodio usando Django ORM"""
        episodio = self.EpisodioCefalea.objects.create(
            paciente=paciente,
            **datos_episodio
        )
        return episodio

    def obtener_episodios_paciente(self, paciente) -> List:
        """Obtener episodios de un paciente"""
        return list(self.EpisodioCefalea.objects.filter(
            paciente=paciente
        ).order_by('-creado_en'))

    def obtener_episodio_por_id(self, episodio_id: int):
        """Obtener episodio por ID"""
        try:
            return self.EpisodioCefalea.objects.get(id=episodio_id)
        except self.EpisodioCefalea.DoesNotExist:
            return None

    def obtener_ultimo_episodio(self, paciente):
        """Obtener último episodio de un paciente"""
        try:
            return self.EpisodioCefalea.objects.filter(
                paciente=paciente
            ).latest('creado_en')
        except self.EpisodioCefalea.DoesNotExist:
            return None

    def contar_episodios_paciente(self, paciente) -> int:
        """Contar episodios de un paciente"""
        return self.EpisodioCefalea.objects.filter(paciente=paciente).count()


class FakeEpisodioCefaleaRepository(AbstractEpisodioCefaleaRepository):
    """
    Repositorio fake para testing BDD usando modelos Django REALES.
    """

    def __init__(self):
        self._episodios = []
        self._next_id = 1
        self._models_loaded = False
        self.EpisodioCefalea = None

    def _load_models(self):
        """Cargar modelos Django solo cuando se necesiten (lazy loading)"""
        if not self._models_loaded:
            from .models import EpisodioCefalea
            self.EpisodioCefalea = EpisodioCefalea
            self._models_loaded = True

    def _get_next_id(self):
        """Generar siguiente ID secuencial"""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def crear_episodio(self, paciente, datos_episodio: Dict[str, Any]):
        """
        Crear episodio usando modelo REAL de Django pero almacenado en memoria.
        """
        self._load_models()

        # Crear episodio REAL usando el modelo de Django
        episodio = self.EpisodioCefalea(
            paciente=paciente,
            **datos_episodio
        )

        # Simular comportamiento de guardado en BD
        episodio.pk = self._get_next_id()
        episodio.id = episodio.pk

        # Simular auto_now_add=True para creado_en
        if not hasattr(episodio, 'creado_en') or not episodio.creado_en:
            episodio.creado_en = timezone.now()

        # "Guardar" en memoria
        self._episodios.append(episodio)

        return episodio

    def obtener_episodios_paciente(self, paciente) -> List:
        """Obtener episodios de un paciente específico"""
        episodios_paciente = [
            ep for ep in self._episodios
            if ep.paciente == paciente
        ]
        # Ordenar por fecha descendente (como en BD real)
        return sorted(episodios_paciente, key=lambda x: x.creado_en, reverse=True)

    def obtener_episodio_por_id(self, episodio_id: int):
        """Obtener episodio por ID"""
        return next(
            (ep for ep in self._episodios if ep.id == episodio_id),
            None
        )

    def obtener_ultimo_episodio(self, paciente):
        """Obtener el último episodio de un paciente"""
        episodios_paciente = self.obtener_episodios_paciente(paciente)
        return episodios_paciente[0] if episodios_paciente else None

    def contar_episodios_paciente(self, paciente) -> int:
        """Contar episodios de un paciente"""
        return len(self.obtener_episodios_paciente(paciente))

    def limpiar_repositorio(self):
        """Limpiar todos los datos (útil para testing)"""
        self._episodios.clear()
        self._next_id = 1

    def obtener_todos_episodios(self) -> List:
        """Obtener todos los episodios (útil para testing)"""
        return self._episodios.copy()
