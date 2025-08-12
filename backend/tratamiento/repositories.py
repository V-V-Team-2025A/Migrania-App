from abc import ABC, abstractmethod
from tratamiento.models import Medicamento, Tratamiento

class BaseMedicamentoRepository(ABC):
    @abstractmethod
    def get_medicamento_by_id(self, id):
        pass

    @abstractmethod
    def get_all_medicamentos(self):
        pass

    @abstractmethod
    def save_medicamento(self, medicamento):
        pass


class BaseTratamientoRepository(ABC):
    @abstractmethod
    def get_tratamiento_by_id(self, id):
        pass

    @abstractmethod
    def get_all_tratamientos(self):
        pass

    @abstractmethod
    def save_tratamiento(self, tratamiento):
        pass

    @abstractmethod
    def add_medicamento_to_tratamiento(self, tratamiento_id, medicamento_id):
        pass

    @abstractmethod
    def get_medicamentos_by_tratamiento_id(self, tratamiento_id):
        pass

class BaseSeguimientoRepository(ABC):
    @abstractmethod
    def get_seguimiento_by_tratamiento_id(self, tratamiento_id):
        pass

    @abstractmethod
    def save_seguimiento(self, seguimiento):
        pass

    @abstractmethod
    def calcular_cumplimiento_tratamiento(self, tratamiento_id):
        pass

class DjangoMedicamentoRepository(BaseMedicamentoRepository):
    def get_medicamento_by_id(self, id):
        try:
            return Medicamento.objects.get(pk=id)
        except Medicamento.DoesNotExist:
            return None

    def get_all_medicamentos(self):
        return Medicamento.objects.all()

    def save_medicamento(self, medicamento):
        medicamento.save()
        return medicamento

class DjangoTratamientoRepository(BaseTratamientoRepository):
    def get_tratamiento_by_id(self, id):
        try:
            return Tratamiento.objects.get(pk=id)
        except Tratamiento.DoesNotExist:
            return None

    def get_all_tratamientos(self):
        return Tratamiento.objects.all()

    def save_tratamiento(self, tratamiento):
        tratamiento.save()
        return tratamiento

    def add_medicamento_to_tratamiento(self, tratamiento_id, medicamento_id):
        tratamiento = self.get_tratamiento_by_id(tratamiento_id)
        medicamento = Medicamento.objects.get(pk=medicamento_id)
        if tratamiento and medicamento:
            tratamiento.medicamentos.add(medicamento)
            return True
        return False

    def get_medicamentos_by_tratamiento_id(self, tratamiento_id):
        tratamiento = self.get_tratamiento_by_id(tratamiento_id)
        if tratamiento:
            return list(tratamiento.medicamentos.all())
        return []

class DjangoSeguimientoRepository(BaseSeguimientoRepository):
    def get_seguimiento_by_tratamiento_id(self, tratamiento_id):
        try:
            tratamiento = Tratamiento.objects.get(pk=tratamiento_id)
            return tratamiento  # Por ahora el seguimiento está en el mismo tratamiento
        except Tratamiento.DoesNotExist:
            return None

    def save_seguimiento(self, seguimiento):
        # Si el seguimiento es parte del tratamiento
        if hasattr(seguimiento, 'save'):
            seguimiento.save()
        return seguimiento

    def calcular_cumplimiento_tratamiento(self, tratamiento_id):
        try:
            tratamiento = Tratamiento.objects.get(pk=tratamiento_id)
            return tratamiento.calcular_cumplimiento()
        except Tratamiento.DoesNotExist:
            return 0.0

class FakeMedicamentoRepository(BaseMedicamentoRepository):
    def __init__(self):
        self.medicamentos = {}
        self.next_id = 1

    def _get_next_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def get_medicamento_by_id(self, id):
        return self.medicamentos.get(id)

    def get_all_medicamentos(self):
        return list(self.medicamentos.values())

    def save_medicamento(self, medicamento):
        if not medicamento.id:
            medicamento.id = self._get_next_id()
        self.medicamentos[medicamento.id] = medicamento
        return medicamento

    def delete_medicamento(self, id):
        if id in self.medicamentos:
            del self.medicamentos[id]
            return True
        return False

class FakeTratamientoRepository(BaseTratamientoRepository):
    def __init__(self, medicamento_repository=None):
        self.tratamientos = {}
        self.tratamiento_medicamentos = {}  # tratamiento_id -> set(medicamento_ids)
        self.next_id = 1
        self.medicamento_repository = medicamento_repository

    def _get_next_id(self):
        id = self.next_id
        self.next_id += 1
        return id

    def get_tratamiento_by_id(self, id):
        return self.tratamientos.get(id)

    def get_all_tratamientos(self):
        return list(self.tratamientos.values())

    def save_tratamiento(self, tratamiento):
        if not tratamiento.id:
            tratamiento.id = self._get_next_id()
            self.tratamiento_medicamentos[tratamiento.id] = set()
        self.tratamientos[tratamiento.id] = tratamiento
        return tratamiento

    def add_medicamento_to_tratamiento(self, tratamiento_id, medicamento_id):
        if tratamiento_id in self.tratamientos:
            if tratamiento_id not in self.tratamiento_medicamentos:
                self.tratamiento_medicamentos[tratamiento_id] = set()
            self.tratamiento_medicamentos[tratamiento_id].add(medicamento_id)
            return True
        return False

    def get_medicamentos_by_tratamiento_id(self, tratamiento_id):
        ids = self.tratamiento_medicamentos.get(tratamiento_id, set())
        if self.medicamento_repository:
            return [self.medicamento_repository.get_medicamento_by_id(mid)
                   for mid in ids if self.medicamento_repository.get_medicamento_by_id(mid)]
        return list(ids)  # Devuelve solo los IDs si no hay repo de medicamentos


class FakeSeguimientoRepository(BaseSeguimientoRepository):
    def __init__(self, tratamiento_repository: BaseTratamientoRepository):
        self.episodios = {}
        self.estadisticas_cumplimiento = {}
        self.next_id = 1
        self.tratamiento_repository = tratamiento_repository

    def _get_next_id(self):
        _id = self.next_id
        self.next_id += 1
        return _id

    # ==== Métodos de la interfaz ====
    def get_seguimiento_by_tratamiento_id(self, tratamiento_id):
        """
        En este fake consideramos que 'seguimiento' es el mismo tratamiento.
        """
        return self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)

    def save_seguimiento(self, seguimiento):
        """
        Guarda un episodio de seguimiento.
        """
        if not getattr(seguimiento, "id", None):
            seguimiento.id = self._get_next_id()
        self.episodios[seguimiento.id] = seguimiento
        return seguimiento

    def calcular_cumplimiento_tratamiento(self, tratamiento_id):
        """
        Retorna el porcentaje de cumplimiento de un tratamiento.
        Si no existe, devuelve 0.0.
        """
        estadisticas = self.estadisticas_cumplimiento.get(tratamiento_id)
        if estadisticas and "porcentaje_cumplimiento" in estadisticas:
            return estadisticas["porcentaje_cumplimiento"]
        return 0.0

    def save_estadisticas_cumplimiento(self, tratamiento_id, estadisticas):
        """
        Guarda estadísticas de cumplimiento.
        Espera un dict con al menos: {'porcentaje_cumplimiento': float, ...}
        """
        if "porcentaje_cumplimiento" not in estadisticas:
            raise ValueError("Las estadísticas deben incluir 'porcentaje_cumplimiento'")
        self.estadisticas_cumplimiento[tratamiento_id] = estadisticas
        return estadisticas

    def get_estadisticas_cumplimiento(self, tratamiento_id):
        """
        Retorna el dict completo de estadísticas, o None si no existe.
        """
        return self.estadisticas_cumplimiento.get(tratamiento_id)

    def get_episodios_by_paciente(self, paciente_id):
        """
        Retorna todos los episodios registrados para un paciente.
        """
        return [
            episodio for episodio in self.episodios.values()
            if getattr(episodio, 'paciente_id', None) == paciente_id
        ]