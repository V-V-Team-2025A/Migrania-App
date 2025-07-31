from django.db import models
import datetime
from faker import Faker
fake = Faker('es_ES')


# Create your models here.
class Medicacion:
    """Representa una medicación con sus atributos."""
    def _init_(self, cantidad, nombre, caracteristica, frecuencia, duracion):
        self.cantidad = cantidad
        self.nombre = nombre
        self.caracteristica = caracteristica
        self.frecuencia = frecuencia
        self.duracion = duracion

    def _eq_(self, other):
        """Compara si dos objetos Medicacion son iguales."""
        return (self.cantidad == other.cantidad and
                self.nombre == other.nombre and
                self.caracteristica == other.caracteristica and
                self.frecuencia == other.frecuencia and
                self.duracion == other.duracion)


class Recomendacion:
    """Representa una recomendación para el tratamiento."""
    def _init_(self, descripcion):
        self.descripcion = descripcion

    def _eq_(self, other):
        """Compara si dos objetos Recomendacion son iguales."""
        return self.descripcion == other.descripcion


class Tratamiento:
    """
    Representa un tratamiento médico, incluyendo medicaciones y recomendaciones.
    Los tratamientos son ingresados por el médico.
    """
    def _init_(self, id_tratamiento=None):
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

class Migrana:
    """Representa un episodio de migraña con su tipo."""
    def _init_(self, tipo):
        self.tipo = tipo
        self.fecha = fake.date_time_this_year()

class Paciente:
    """Representa un paciente con su historial médico y tratamientos."""
    def _init_(self, nombre=None, id_paciente=None):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.historial_migranas = []
        self.tratamientos_activos = []
        self.historial_alertas_tomas = {} # {id_tratamiento: [fecha_toma_confirmada, ...]}

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
        self.historial_alertas_tomas[id_tratamiento].append(fecha_toma if fecha_toma else datetime.now())

    def simular_historial_tomas(self, id_tratamiento, porcentaje_cumplimiento, tomas_esperadas_simuladas=100):
        """
        Simula el historial de tomas para un tratamiento dado.
        Esta es la lógica de negocio que prepara los datos para el cálculo.
        """
        tomas_confirmadas = int((float(porcentaje_cumplimiento) / 100) * tomas_esperadas_simuladas)
        self.historial_alertas_tomas[id_tratamiento] = {
            'tomas_confirmadas': tomas_confirmadas,
            'tomas_esperadas': tomas_esperadas_simuladas
        }

    def obtener_porcentaje_cumplimiento(self, id_tratamiento):
        if id_tratamiento not in self.historial_alertas_tomas:
            return 0.0

        data = self.historial_alertas_tomas[id_tratamiento]
        tomas_confirmadas = data['tomas_confirmadas']
        tomas_esperadas = data['tomas_esperadas']

        if tomas_esperadas == 0:
            return 100.0  # Si no hay tomas esperadas, se considera 100% de cumplimiento
        return (tomas_confirmadas / tomas_esperadas) * 100