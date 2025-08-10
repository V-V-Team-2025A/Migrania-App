from django.utils import timezone
from tratamiento.models import Medicamento

class MedicamentoService:
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


    def agregar_medicamento_a_tratamiento(self, tratamiento_id, medicamento):
        """Agregar un medicamento al tratamiento"""
        tratamiento = self.tratamiento_repository.get_tratamiento_by_id(tratamiento_id)
        if not tratamiento:
            return False

        # Si el medicamento no existe, lo guardamos primero
        if not medicamento.id:
            medicamento = self.tratamiento_repository.save_medicamento(medicamento)

        return self.tratamiento_repository.add_medicamento_to_tratamiento(tratamiento_id, medicamento.id)







