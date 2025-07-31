from django.db import models
import datetime
from faker import Faker
fake = Faker('es_ES')

class Medicacion:
    """Representa una medicación con sus atributos."""
    def __init__(self, cantidad, nombre, caracteristica, frecuencia, duracion):
        self.cantidad = cantidad
        self.nombre = nombre
        self.caracteristica = caracteristica
        self.frecuencia = frecuencia
        self.duracion = duracion

    def __eq__(self, other):
        if not isinstance(other, Medicacion):
            return False
        return (
            self.cantidad == other.cantidad and
            self.nombre == other.nombre and
            self.caracteristica == other.caracteristica and
            self.frecuencia == other.frecuencia and
            self.duracion == other.duracion
        )

    def __repr__(self):
        return (f"<Medicacion nombre={self.nombre!r} cantidad={self.cantidad!r} "
                f"caracteristica={self.caracteristica!r} frecuencia={self.frecuencia!r} "
                f"duracion={self.duracion!r}>")


class Recomendacion:
    """Representa una recomendación para el tratamiento."""
    def __init__(self, descripcion):
        self.descripcion = descripcion

    def __eq__(self, other):
        if not isinstance(other, Recomendacion):
            return False
        return self.descripcion == other.descripcion

    def __repr__(self):
        return f"<Recomendacion descripcion={self.descripcion!r}>"


class Tratamiento:
    """
    Representa un tratamiento médico, incluyendo medicaciones y recomendaciones.
    Los tratamientos son ingresados por el médico.
    """
    def __init__(self, id_tratamiento=None):
        self.id_tratamiento = id_tratamiento if id_tratamiento else fake.uuid4()
        self.medicaciones = []
        self.recomendaciones = []
        self.activo = True
        self.cumplimiento = 0.0
        self.motivo_cancelacion = None

    def agregar_medicacion(self, medicacion):
        """Agrega una medicación al tratamiento."""
        self.medicaciones.append(medicacion)

    def agregar_recomendacion(self, recomendacion):
        """Agrega una recomendación al tratamiento."""
        self.recomendaciones.append(recomendacion)

    def cancelar_tratamiento(self, motivo):
        """Cancela el tratamiento y registra el motivo."""
        self.activo = False
        self.motivo_cancelacion = motivo

    def modificar_tratamiento(self, nuevas_medicaciones, nuevas_recomendaciones):
        """Modifica el tratamiento con nuevas medicaciones y recomendaciones."""
        self.medicaciones = nuevas_medicaciones
        self.recomendaciones = nuevas_recomendaciones

    def __repr__(self):
        return (f"<Tratamiento id={self.id_tratamiento} activo={self.activo} "
                f"medicaciones={len(self.medicaciones)} recomendaciones={len(self.recomendaciones)}>")


class Migrana:
    """Representa un episodio de migraña con su tipo."""
    def __init__(self, tipo):
        self.tipo = tipo
        self.fecha = fake.date_time_this_year()

    def __repr__(self):
        return f"<Migrana tipo={self.tipo!r} fecha={self.fecha.isoformat()}>"


class Paciente:
    """Representa un paciente con su historial médico y tratamientos."""
    def __init__(self, nombre=None, id_paciente=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.historial_migranas = []
        self.tratamientos_activos = []
        self.historial_alertas_tomas = {}  # {id_tratamiento: [fecha_toma_confirmada, ...]}

    def agregar_migrana(self, migrana):
        """Agrega un episodio de migraña al historial del paciente."""
        self.historial_migranas.append(migrana)

    def agregar_tratamiento_activo(self, tratamiento):
        """Agrega un tratamiento activo al paciente."""
        self.tratamientos_activos.append(tratamiento)

    def registrar_toma_confirmada(self, id_tratamiento, fecha_toma=None):
        """Registra una toma confirmada para un tratamiento específico."""
        if id_tratamiento not in self.historial_alertas_tomas:
            self.historial_alertas_tomas[id_tratamiento] = []
        self.historial_alertas_tomas[id_tratamiento].append(
            fecha_toma if fecha_toma else datetime.datetime.now()
        )

    def simular_historial_tomas(self, id_tratamiento, porcentaje_cumplimiento, tomas_esperadas_simuladas=100):
        """
        Simula el historial de tomas para un tratamiento dado.
        Esta es la lógica de negocio que prepara los datos para el cálculo.
        """
        tomas_confirmadas = int((float(porcentaje_cumplimiento) / 100.0) * tomas_esperadas_simuladas)
        self.historial_alertas_tomas[id_tratamiento] = {
            "tomas_confirmadas": tomas_confirmadas,
            "tomas_esperadas": tomas_esperadas_simuladas,
        }

    def obtener_porcentaje_cumplimiento(self, id_tratamiento):
        if id_tratamiento not in self.historial_alertas_tomas:
            return 0.0

        data = self.historial_alertas_tomas[id_tratamiento]
        tomas_confirmadas = data.get("tomas_confirmadas", 0)
        tomas_esperadas = data.get("tomas_esperadas", 0)

        if tomas_esperadas == 0:
            return 100.0  # Si no hay tomas esperadas, se considera 100% de cumplimiento
        return (tomas_confirmadas / tomas_esperadas) * 100.0

    def __repr__(self):
        return (f"<Paciente nombre={self.nombre!r} id={self.id_paciente!r} "
                f"migranas={len(self.historial_migranas)} tratamientos={len(self.tratamientos_activos)}>")
