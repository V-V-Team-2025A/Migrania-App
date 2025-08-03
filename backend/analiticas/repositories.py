# repositories.py

from abc import ABC, abstractmethod
from typing import List
from collections import defaultdict
from analiticas.analisis_patrones_data_structures import EpisodioData

class AnalisisPatronesRepository(ABC):
    """
    Interfaz del repositorio para el módulo de análisis.
    Define cómo se guardan y recuperan los datos de episodios para el análisis.
    """
    @abstractmethod
    def guardar_episodio(self, paciente_id: int, episodio: EpisodioData):
        pass

    @abstractmethod
    def obtener_episodios_por_paciente(self, paciente_id: int) -> List[EpisodioData]:
        pass


class FakeAnalisisPatronesRepository(AnalisisPatronesRepository):
    """
    Implementación en memoria (Fake) del repositorio.
    Es completamente independiente y gestiona su propia colección de datos.
    """
    def __init__(self):
        # Usamos un defaultdict para inicializar una lista vacía para nuevos pacientes
        self._episodios_por_paciente = defaultdict(list)

    def guardar_episodio(self, paciente_id: int, episodio: EpisodioData):
        """Guarda un episodio de prueba en la lista de un paciente."""
        episodio.paciente_id = paciente_id
        self._episodios_por_paciente[paciente_id].append(episodio)

    def obtener_episodios_por_paciente(self, paciente_id: int) -> List[EpisodioData]:
        """Devuelve la lista de episodios guardados para un paciente."""
        return self._episodios_por_paciente.get(paciente_id, [])

