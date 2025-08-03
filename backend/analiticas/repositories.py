import abc
from typing import Dict, List, Optional, Any
from datetime import date


class AbstractEstadisticaHistorialRepository(abc.ABC):
    """Contrato base para repositorio de estadísticas historial"""

    @abc.abstractmethod
    def calcular_promedio_semanal(self, total_episodios: int, fecha_inicio: date, fecha_fin: date) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def calcular_duracion_promedio(self, total_episodios: int, suma_duracion_total: float) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    def calcular_intensidad_promedio(self, intensidades: List[int] = None) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def calcular_asociacion_hormonal(self, total_episodios: int, episodios_menstruacion: int, 
                                   episodios_anticonceptivos: int) -> tuple:
        raise NotImplementedError

    @abc.abstractmethod
    def calcular_evolucion_midas(self, puntuacion_promedio: float, puntuacion_actual: float) -> tuple:
        raise NotImplementedError

    @abc.abstractmethod
    def calcular_desencadenantes_comunes(self, desencadenantes_dict: Dict[str, int]) -> List[tuple]:
        raise NotImplementedError


class DjangoEstadisticaHistorialRepository(AbstractEstadisticaHistorialRepository):
    """Implementación Django del repositorio de estadísticas historial"""

    def calcular_promedio_semanal(self, total_episodios: int, fecha_inicio: date, fecha_fin: date) -> float:
        from .models import PromedioSemanalEpisodios
        return PromedioSemanalEpisodios.calcular_promedio(total_episodios, fecha_inicio, fecha_fin)

    def calcular_duracion_promedio(self, total_episodios: int, suma_duracion_total: float) -> float:
        from .models import DuracionPromedioEpisodios
        return DuracionPromedioEpisodios.calcular_duracion_promedio(total_episodios, suma_duracion_total)

    def calcular_intensidad_promedio(self, intensidades: List[int] = None) -> str:
        from .models import IntensidadPromedioDolor
        if intensidades:
            return IntensidadPromedioDolor.calcular_intensidad_promedio(intensidades)
        return IntensidadPromedioDolor.obtener_intensidad_promedio()

    def calcular_asociacion_hormonal(self, total_episodios: int, episodios_menstruacion: int, 
                                   episodios_anticonceptivos: int) -> tuple:
        from .models import AsociacionHormonal
        return AsociacionHormonal.calcular_porcentajes(total_episodios, episodios_menstruacion, episodios_anticonceptivos)

    def calcular_evolucion_midas(self, puntuacion_promedio: float, puntuacion_actual: float) -> tuple:
        from .models import EvolucionMIDAS
        return EvolucionMIDAS.calcular_evolucion(puntuacion_promedio, puntuacion_actual)

    def calcular_desencadenantes_comunes(self, desencadenantes_dict: Dict[str, int]) -> List[tuple]:
        from .models import DesencadenantesComunes
        return DesencadenantesComunes.calcular_desencadenantes_frecuentes(desencadenantes_dict)