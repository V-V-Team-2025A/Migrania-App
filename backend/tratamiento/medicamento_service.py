from django.utils import timezone
from tratamiento.models import Medicamento

class MedicamentoService:
    def __init__(self, repository):
        self.tratamiento_repository = repository

    def crear_medicamento(self, nombre, dosis, caracteristica, hora_inicio, frecuencia_horas, duracion_dias):
        """Crear un nuevo medicamento"""
        errores = self._validar_datos_medicamento(nombre, dosis, caracteristica, hora_inicio, frecuencia_horas,
                                                  duracion_dias)
        if errores:
            raise ValueError(f"Datos de medicamento inválidos: {', '.join(errores)}")

        medicamento = Medicamento(
            nombre=nombre,
            dosis=dosis,
            caracteristica=caracteristica,
            hora_de_inicio=hora_inicio,
            frecuencia_horas=frecuencia_horas,
            duracion_dias=duracion_dias
        )
        return self.tratamiento_repository.save_medicamento(medicamento)

    def _validar_datos_medicamento(self, nombre, dosis, caracteristica, hora_inicio, frecuencia_horas, duracion_dias):
        """Validar datos del medicamento según reglas de negocio"""
        errores = []

        # Validar nombre
        if not nombre or not isinstance(nombre, str) or len(nombre.strip()) == 0:
            errores.append("El nombre del medicamento es obligatorio")
        elif len(nombre.strip()) > 100:
            errores.append("El nombre del medicamento no puede exceder 100 caracteres")

        # Validar dosis
        if not dosis or not isinstance(dosis, str) or len(dosis.strip()) == 0:
            errores.append("La dosis es obligatoria")
        elif len(dosis.strip()) > 50:
            errores.append("La dosis no puede exceder 50 caracteres")

        # Validar característica (opcional pero si se proporciona debe ser válida)
        if caracteristica is not None and len(str(caracteristica).strip()) > 100:
            errores.append("Las características no pueden exceder 100 caracteres")

        # Validar frecuencia
        if not isinstance(frecuencia_horas, int) or frecuencia_horas <= 0:
            errores.append("La frecuencia debe ser un número entero positivo")
        elif frecuencia_horas > 24:
            errores.append("La frecuencia no puede ser mayor a 24 horas")

        # Validar duración
        if not isinstance(duracion_dias, int) or duracion_dias <= 0:
            errores.append("La duración debe ser un número entero positivo")
        elif duracion_dias > 365:
            errores.append("La duración del tratamiento no puede exceder 365 días")

        # Validar hora de inicio
        if hora_inicio is None:
            errores.append("La hora de inicio es obligatoria")

        return errores







