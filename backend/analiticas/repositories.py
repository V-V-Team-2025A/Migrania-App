# analiticas/repositories.py

import abc
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import date
from .analisis_patrones_data_structures import EpisodioData
from evaluacion_diagnostico.models import EpisodioCefalea


# Repositorios para Análisis de Patrones
class AnalisisPatronesRepository(ABC):
    """Interfaz del repositorio para análisis de patrones."""

    @abstractmethod
    def obtener_episodios_por_paciente(self, paciente_id: int) -> List[EpisodioData]:
        pass

    @abstractmethod
    def guardar_episodio(self, paciente_id: int, episodio: EpisodioData):
        pass


# Repositorios para Estadísticas Historial
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


class FakeEstadisticaHistorialRepository(AbstractEstadisticaHistorialRepository):
    """
    Repositorio FAKE para testing BDD - NO guarda en BD.
    Simula el consumo de APIs de evaluacion_diagnostico (bitácora y MIDAS)
    y calcula estadísticas en memoria usando los modelos.
    """

    def __init__(self):
        self._episodios_simulados = []
        self._evaluaciones_midas_simuladas = []
        self._models_loaded = False

    def _load_models(self):
        """Cargar modelos Django solo cuando se necesiten (lazy loading)"""
        if not self._models_loaded:
            from .models import (
                PromedioSemanalEpisodios, 
                DuracionPromedioEpisodios, 
                IntensidadPromedioDolor,
                AsociacionHormonal, 
                EvolucionMIDAS, 
                DesencadenantesComunes
            )
            self.PromedioSemanalEpisodios = PromedioSemanalEpisodios
            self.DuracionPromedioEpisodios = DuracionPromedioEpisodios
            self.IntensidadPromedioDolor = IntensidadPromedioDolor
            self.AsociacionHormonal = AsociacionHormonal
            self.EvolucionMIDAS = EvolucionMIDAS
            self.DesencadenantesComunes = DesencadenantesComunes
            self._models_loaded = True

    def calcular_promedio_semanal(self, total_episodios: int, fecha_inicio: date, fecha_fin: date) -> float:
        """Usa el modelo para calcular promedio semanal sin guardar en BD"""
        self._load_models()
        return self.PromedioSemanalEpisodios.calcular_promedio(total_episodios, fecha_inicio, fecha_fin)

    def calcular_duracion_promedio(self, total_episodios: int, suma_duracion_total: float) -> float:
        """Usa el modelo para calcular duración promedio sin guardar en BD"""
        self._load_models()
        return self.DuracionPromedioEpisodios.calcular_duracion_promedio(total_episodios, suma_duracion_total)

    def calcular_intensidad_promedio(self, intensidades: List[int] = None) -> str:
        """Usa el modelo para determinar intensidad promedio sin guardar en BD"""
        self._load_models()
        if intensidades:
            return self.IntensidadPromedioDolor.obtener_intensidad_promedio()
        return self.IntensidadPromedioDolor.obtener_intensidad_promedio()

    def calcular_asociacion_hormonal(self, total_episodios: int, episodios_menstruacion: int, 
                                   episodios_anticonceptivos: int) -> tuple:
        """Usa el modelo para calcular asociación hormonal sin guardar en BD"""
        self._load_models()
        return self.AsociacionHormonal.calcular_porcentajes(
            total_episodios, episodios_menstruacion, episodios_anticonceptivos
        )

    def calcular_evolucion_midas(self, puntuacion_promedio: float, puntuacion_actual: float) -> tuple:
        """Usa el modelo para calcular evolución MIDAS sin guardar en BD"""
        self._load_models()
        return self.EvolucionMIDAS.calcular_evolucion(puntuacion_promedio, puntuacion_actual)

    def calcular_desencadenantes_comunes(self, desencadenantes_dict: Dict[str, int]) -> List[tuple]:
        """Usa el modelo para calcular desencadenantes comunes sin guardar en BD"""
        self._load_models()
        return self.DesencadenantesComunes.calcular_desencadenantes_frecuentes(desencadenantes_dict)


# Implementaciones para Análisis de Patrones
class FakeAnalisisPatronesRepository(AnalisisPatronesRepository):
    def __init__(self):
        self._episodios = {}

    def guardar_episodio(self, paciente_id: int, episodio: EpisodioData):
        if paciente_id not in self._episodios:
            self._episodios[paciente_id] = []
        self._episodios[paciente_id].append(episodio)

    def obtener_episodios_por_paciente(self, paciente_id: int) -> List[EpisodioData]:
        return self._episodios.get(paciente_id, [])


class DjangoAnalisisPatronesRepository(AnalisisPatronesRepository):
    """
    Implementación real que interactúa con la base de datos de Django.
    """

    def obtener_episodios_por_paciente(self, paciente_id: int) -> List[EpisodioData]:
        episodios_orm = EpisodioCefalea.objects.filter(paciente_id=paciente_id).order_by('-creado_en')[:50]
        episodios_data = []
        for orm_obj in episodios_orm:
            data = EpisodioData(
                localizacion=orm_obj.localizacion,
                caracter_dolor=orm_obj.caracter_dolor,
                empeora_actividad=bool(orm_obj.empeora_actividad),
                severidad=orm_obj.severidad,
                nauseas_vomitos=bool(orm_obj.nauseas_vomitos),
                fotofobia=bool(orm_obj.fotofobia),
                fonofobia=bool(orm_obj.fonofobia),
                presencia_aura=bool(orm_obj.presencia_aura),
                sintomas_aura=orm_obj.sintomas_aura,
                duracion_aura_minutos=orm_obj.duracion_aura_minutos,
                en_menstruacion=bool(orm_obj.en_menstruacion),
                categoria_diagnostica=orm_obj.categoria_diagnostica,
                dia=orm_obj.creado_en.strftime('%A'),
                fecha_creacion=orm_obj.creado_en,
                paciente_id=orm_obj.paciente_id
            )
            episodios_data.append(data)
        return episodios_data

    def guardar_episodio(self, paciente_id: int, episodio: EpisodioData):
        """
        Este repositorio es de solo lectura. Este método no se usa en producción.
        Se implementa solo para cumplir con el contrato de la clase abstracta.
        """
        raise NotImplementedError("El repositorio de análisis es de solo lectura.")
