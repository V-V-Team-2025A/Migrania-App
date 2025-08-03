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
            # TODO: Implementar lógica real cuando tengamos más datos
            # Por ahora retorna el método del modelo
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

    def simular_episodios_desde_api_bitacora(self, paciente_id: int, cantidad: int = 10):
        """
        Simula el consumo de la API de bitácora digital de evaluacion_diagnostico
        En el futuro, aquí haríamos requests.get() a los endpoints
        """
        # Simulamos episodios que vendrían de la API
        episodios_simulados = []
        for i in range(cantidad):
            episodio = {
                'id': i + 1,
                'paciente_id': paciente_id,
                'duracion_cefalea_horas': fake.random_int(min=2, max=24),
                'severidad': fake.random_element(elements=['Leve', 'Moderada', 'Severa']),
                'en_menstruacion': fake.boolean(chance_of_getting_true=30),
                'anticonceptivos': fake.boolean(chance_of_getting_true=25),
                'creado_en': fake.date_between(start_date='-3m', end_date='today')
            }
            episodios_simulados.append(episodio)
        
        self._episodios_simulados = episodios_simulados
        return episodios_simulados

    def simular_evaluaciones_midas_desde_api(self, paciente_id: int, cantidad: int = 3):
        """
        Simula el consumo de la API de evaluaciones MIDAS de evaluacion_diagnostico
        En el futuro, aquí haríamos requests.get() a los endpoints
        """
        # Simulamos evaluaciones MIDAS que vendrían de la API
        evaluaciones_simuladas = []
        for i in range(cantidad):
            evaluacion = {
                'id': i + 1,
                'paciente_id': paciente_id,
                'puntaje_total': fake.random_int(min=0, max=50),
                'fecha_evaluacion': fake.date_between(start_date='-6m', end_date='today')
            }
            evaluaciones_simuladas.append(evaluacion)
        
        self._evaluaciones_midas_simuladas = evaluaciones_simuladas
        return evaluaciones_simuladas

    def limpiar_simulaciones(self):
        """Útil para resetear entre escenarios BDD"""
        self._episodios_simulados.clear()
        self._evaluaciones_midas_simuladas.clear()


# Importar Faker para simulaciones
from faker import Faker
fake = Faker('es_ES')