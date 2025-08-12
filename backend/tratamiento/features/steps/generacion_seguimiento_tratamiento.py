import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "migraine_app.settings")
django.setup()

from behave import *
from django.utils import timezone
from datetime import datetime, date
from faker import Faker

from usuarios.repositories import FakeUserRepository
from evaluacion_diagnostico.repositories import FakeEpisodioCefaleaRepository
from evaluacion_diagnostico.episodio_cefalea_service import EpisodioCefaleaService

from tratamiento.repositories import FakeTratamientoRepository
from tratamiento.tratamiento_service import TratamientoService
from tratamiento.medicamento_service import MedicamentoService
from tratamiento.seguimiento_services import SeguimientoService
from tratamiento.models import Recomendacion

use_step_matcher("re")
fake = Faker('es_ES')

@step("que el paciente tiene al menos un historial de migrañas")
def step_historial_migranas(context):
    inicializar_contexto_basico(context)

    episodio_prev = crear_episodio_de_prueba(
        context,
        paciente=context.paciente.usuario,
        tipo_migraña="Migraña sin aura",
    )
    context.historial_episodios = [episodio_prev]
    context.tiene_historial = True

    assert context.paciente is not None, "No se creó el paciente en el contexto."
    assert episodio_prev is not None, "No se pudo crear el episodio previo."
    assert context.historial_episodios and len(context.historial_episodios) >= 1, \
        "Se esperaba al menos un episodio en el historial."


@step(r"que el paciente presenta su primer episodio con la categorización (.+)")
def step_primer_episodio(context, tipo_migrana):
    # Asegura paciente en contexto
    if not getattr(context, "paciente", None):
        inicializar_contexto_basico(context)

    tipo = tipo_migrana.strip()

    # Crea episodio con datos coherentes al tipo
    context.episodio = crear_episodio_de_prueba(
        context,
        paciente=context.paciente.usuario,
        tipo_migraña=tipo
    )

    if hasattr(context.episodio, "categoria_diagnostica"):
        assert _norm(context.episodio.categoria_diagnostica) == _norm(tipo), \
            f'La categorización del episodio ("{getattr(context.episodio, "categoria_diagnostica", None)}") ' \
            f'no coincide con la recibida ("{tipo}").'


@step("el médico ingresa los datos del tratamiento")
def step_ingresar_datos(context):
    context.tratamiento_repository = FakeTratamientoRepository()
    context.tratamiento_service = TratamientoService(context.tratamiento_repository)
    context.medicamento_service = MedicamentoService(context.tratamiento_repository)

    # Datos deterministas
    dosis = "500mg"
    medicamento_nombre = "Ibuprofeno"
    duracion_dias = 7
    caracteristica = "Tabletas"
    frecuencia_horas = 8

    # 1) Crear tratamiento activo
    context.tratamiento = context.tratamiento_service.crear_tratamiento(
        paciente=context.paciente,
        episodio=context.episodio,
        activo=True,
        fecha_inicio=date.today(),
    )

    # 2) Sincronizar en repo fake ANTES de agregar medicamento
    context.tratamiento_repository.save_tratamiento(context.tratamiento)

    # 3) Crear y agregar medicamento
    context.medicamento = context.medicamento_service.crear_medicamento(
        nombre=medicamento_nombre,
        dosis=dosis,
        caracteristica=caracteristica,
        hora_inicio=timezone.now().time(),
        frecuencia_horas=frecuencia_horas,
        duracion_dias=duracion_dias
    )
    tratamiento = context.tratamiento_service.agregar_medicamento_a_tratamiento(
        context.tratamiento.id, context.medicamento
    )
    assert tratamiento, "No se pudo agregar el medicamento al tratamiento (repo no encontró el tratamiento)."

    # 4) Al menos una recomendación (JSONField como lista de strings)
    context.tratamiento.recomendaciones = [Recomendacion.HIDRATACION.value]  # "hidratacion"
    context.tratamiento_repository.save_tratamiento(context.tratamiento)

    context.tratamiento_creado = context.tratamiento


@step("el sistema crea el tratamiento")
def step_crea_tratamiento(context):
    assert hasattr(context, 'tratamiento_creado'), "El tratamiento debió ser creado en el step anterior"
    assert context.tratamiento_creado is not None, "El tratamiento no puede ser None"

    tratamiento_repositorio = context.tratamiento_repository.get_tratamiento_by_id(context.tratamiento_creado.id)
    medicamentos_tratamiento = context.tratamiento_repository.get_medicamentos_by_tratamiento_id(
        context.tratamiento_creado.id
    )

    assert len(medicamentos_tratamiento) >= 1, "El tratamiento debe tener al menos una medicación"
    assert isinstance(tratamiento_repositorio.recomendaciones, list) and len(tratamiento_repositorio.recomendaciones) >= 1, \
        "El tratamiento debe tener al menos una recomendación"

    assert context.tratamiento_creado.activo is True, "El tratamiento debe estar activo"
    assert context.tratamiento_creado.esta_activo() is True, "El tratamiento debe estar en estado activo"

    context.tratamiento_generado = context.tratamiento_creado


@step("que el paciente tiene un tratamiento activo correspondiente a un episodio médico")
def step_paciente_con_tratamiento(context):
    if not getattr(context, "paciente", None):
        inicializar_contexto_basico(context)
    if not getattr(context, "episodio", None):
        context.episodio = crear_episodio_de_prueba(
            context,
            paciente=context.paciente.usuario,
            tipo_migraña=getattr(context, 'tipo_migraña_actual', 'Migraña sin aura')
        )

    context.tratamiento_repository = FakeTratamientoRepository()
    context.tratamiento_service = TratamientoService(context.tratamiento_repository)

    context.tratamiento_activo = context.tratamiento_service.crear_tratamiento(
        paciente=context.paciente,
        episodio=context.episodio,
        fecha_inicio=datetime.now().date(),
        activo=True
    )
    # sincroniza en repo por si el service devolvió uno existente
    context.tratamiento_repository.save_tratamiento(context.tratamiento_activo)
    assert context.tratamiento_activo.esta_activo(), "El tratamiento no está activo."


@step(
    "el historial de alertas indica que el paciente ha confirmado (?P<porcentaje_cumplimiento>.+)% de las tomas correspondientes a (?P<numero_tratamientos>.+) tratamientos")
def step_historial_cumplimiento(context, porcentaje_cumplimiento, numero_tratamientos):
    context.porcentaje_cumplimiento = float(porcentaje_cumplimiento)

    # Asegurar tratamiento activo en contexto
    if not getattr(context, "tratamiento_activo", None):
        step_paciente_con_tratamiento(context)

    context.tratamiento_activo.cumplimiento = context.porcentaje_cumplimiento
    context.tratamiento_repository.save_tratamiento(context.tratamiento_activo)
    assert context.tratamiento_activo is not None, "El primer tratamiento debe existir."


@step("el médico evalúa el cumplimiento del tratamiento anterior")
def step_medico_evalua(context):

    context.seguimiento_service = SeguimientoService(context.tratamiento_service)

    tratamiento = getattr(context, "tratamiento_activo", None)
    if not tratamiento:
        raise ValueError("No hay tratamiento activo para evaluar cumplimiento")

    evaluacion = context.seguimiento_service.evaluar_cumplimiento(tratamiento.id)

    context.evaluacion_cumplimiento = evaluacion
    context.cumplimiento_evaluado = True

    assert context.cumplimiento_evaluado is True, "La evaluación debe estar completada."


@step("se decide modificar el tratamiento")
def step_modificar_tratamiento(context):
    porcentaje = context.evaluacion_cumplimiento.get('porcentaje', 0.0)
    accion = context.seguimiento_service.decidir_accion_seguimiento(porcentaje)

    assert accion == 'modificar', f"Con {porcentaje}% se esperaba 'modificar', se obtuvo '{accion}'"

    # Solo guardamos la decisión
    context.decision_accion = accion

@step("el médico ingresa las siguientes características para el nuevo tratamiento")
def step_medico_ingresa_caracteristicas(context):
    # Generar nuevos datos usando Faker
    context.nueva_cantidad = fake.random_element(['10', '20', '12', '30'])
    context.nueva_medicamento = fake.random_element(['Ibuprofeno', 'Paracetamol', 'Sumatriptán'])
    context.nueva_duracion = fake.random_element([3, 15, 8])
    context.caracteristica = fake.random_element(['50mg', '500mg', '10mg'])

    assert context.nueva_cantidad is not None, "La cantidad debe estar definida."
    assert context.nueva_medicamento is not None, "La medicación debe estar definida."


@step("el sistema debe actualizar el tratamiento con los nuevos datos")
def step_sistema_actualiza(context):
    if not getattr(context, "tratamiento_repository", None):
        context.tratamiento_repository = FakeTratamientoRepository()
        context.tratamiento_service = TratamientoService(context.tratamiento_repository)
    if not getattr(context, "tratamiento_activo", None):
        step_paciente_con_tratamiento(context)

    medicamento_service = MedicamentoService(context.tratamiento_repository)

    nuevo_medicamento = medicamento_service.crear_medicamento(
        nombre=context.nueva_medicamento,
        dosis=context.nueva_cantidad,
        caracteristica=context.caracteristica,
        hora_inicio=datetime.now().time(),
        frecuencia_horas=8,
        duracion_dias=context.nueva_duracion
    )
    tratamiento_nuevo = context.tratamiento_service.agregar_medicamento_a_tratamiento(
        context.tratamiento_activo.id,
        nuevo_medicamento
    )
    assert tratamiento_nuevo, "No se pudo agregar el medicamento al tratamiento (repo no encontró el tratamiento)."

    context.tratamiento_repository.save_tratamiento(context.tratamiento_activo)
    context.actualizacion_exitosa = True
    assert context.actualizacion_exitosa is True, "La actualización debe ser exitosa."


@step('se decide cancelar el tratamiento')
def step_cancelar_tratamiento_actual(context):
    porcentaje = context.evaluacion_cumplimiento.get('porcentaje', 0.0)

    assert porcentaje < 80, "El cumplimiento promedio debe ser menor a 80%."

    accion = context.seguimiento_service.decidir_accion_seguimiento(porcentaje)
    assert accion == 'cancelar', f"Con {porcentaje}% se esperaba 'cancelar', se obtuvo '{accion}'"

    context.decision_accion = accion


@step('el médico ingresa el motivo como "(?P<motivo_cancelacion>.+)"')
def step_ingresar_motivo(context, motivo_cancelacion):
    context.motivo_cancelacion = motivo_cancelacion
    assert len(motivo_cancelacion.strip()) > 0, "El motivo no puede estar vacío."


@step("el sistema debe cancelar el tratamiento con los datos ingresados")
def step_cancelar_tratamiento(context):
    tratamiento_a_cancelar = context.tratamiento_repository.get_tratamiento_by_id(context.tratamiento_activo.id)
    tratamiento_a_cancelar.activo = False
    tratamiento_a_cancelar.motivo_cancelacion = context.motivo_cancelacion

    context.tratamiento_repository.save_tratamiento(tratamiento_a_cancelar)

    context.tratamiento_cancelado = tratamiento_a_cancelar
    context.cancelacion_realizada = True

    assert tratamiento_a_cancelar.activo is False, "El tratamiento debe estar inactivo."
    assert context.cancelacion_realizada is True, "La cancelación debe estar realizada."


# Helpers

def inicializar_contexto_basico(context):
    """
    Inicializa el contexto usando repos fakes (NO ORM directo).
    Crea un paciente y un médico de prueba.
    """
    context.fake_repo = FakeUserRepository()

    # Paciente
    user_data_paciente = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'cedula': str(fake.unique.random_number(digits=10, fix_len=True)),
        'telefono': fake.msisdn()[3:13],
        'fecha_nacimiento': fake.date_of_birth(minimum_age=18, maximum_age=80),
        'genero': fake.random_element(['M', 'F']),
        'direccion': fake.address(),
    }
    profile_data_paciente = {
        'grupo_sanguineo': fake.random_element(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
        'contacto_emergencia_nombre': fake.name(),
        'contacto_emergencia_telefono': fake.msisdn()[3:13],
        'contacto_emergencia_relacion': fake.random_element(
            ['Padre', 'Madre', 'Hermano', 'Hermana', 'Cónyuge', 'Hijo', 'Hija'])
    }
    context.usuario_paciente = context.fake_repo.create_paciente(user_data_paciente, profile_data_paciente)
    context.paciente = next(
        (p for p in context.fake_repo.get_all_pacientes() if p.usuario.id == context.usuario_paciente.id),
        None
    )

    # Médico (si lo necesitas)
    user_data_medico = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'cedula': str(fake.unique.random_number(digits=10, fix_len=True)),
        'telefono': fake.msisdn()[3:13],
        'fecha_nacimiento': fake.date_of_birth(minimum_age=25, maximum_age=65),
        'genero': fake.random_element(['M', 'F']),
        'direccion': fake.address(),
    }
    profile_data_medico = {
        'numero_licencia': fake.unique.bothify(text='MED-####'),
        'especializacion': fake.random_element(
            ['cardiologia', 'neurologia', 'pediatria', 'dermatologia', 'ginecologia']),
        'anos_experiencia': fake.random_int(min=1, max=30),
    }
    context.usuario_medico = context.fake_repo.create_medico(user_data_medico, profile_data_medico)
    context.medico = next(
        (m for m in context.fake_repo.get_all_medicos() if m.usuario.id == context.usuario_medico.id),
        None
    )

def _norm(s: str) -> str:
    """Normaliza: minúsculas y sin acentos/espacios dobles."""
    import unicodedata
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.strip().lower().replace("  ", " ")


def _datos_episodio_por_tipo(tipo: str) -> dict:
    """Construye datos de episodio coherentes con la categorización solicitada."""
    t = _norm(tipo)  # ej: "migraña sin aura", "migraña con aura", "cefalea tensional"
    base = {
        'duracion_cefalea_horas': 2,
        'severidad': 'Moderada',
        'categoria_diagnostica': tipo,  # mantenemos la etiqueta pedida
    }

    # 1) Tensional
    if "tensional" in t:
        return {
            **base,
            'localizacion': 'Bilateral',
            'caracter_dolor': 'Opresivo',
            'empeora_actividad': False,
            'nauseas_vomitos': False,
            'fotofobia': False,
            'fonofobia': False,
            'presencia_aura': False,
            'sintomas_aura': '',
            'duracion_aura_minutos': 0,
            'en_menstruacion': False,
            'anticonceptivos': False,
        }

    # 2) Migraña SIN aura (evalúa antes que "con aura" para evitar el false positive por substring)
    if "sin aura" in t or ("sin" in t and "aura" in t):
        return {
            **base,
            'localizacion': 'Unilateral',
            'caracter_dolor': 'Pulsátil',
            'empeora_actividad': True,
            'nauseas_vomitos': True,
            'fotofobia': True,
            'fonofobia': False,
            'presencia_aura': False,
            'sintomas_aura': '',
            'duracion_aura_minutos': 0,
            'en_menstruacion': False,
            'anticonceptivos': False,
        }

    # 3) Migraña CON aura
    if "con aura" in t or ("con" in t and "aura" in t):
        return {
            **base,
            'localizacion': 'Unilateral',
            'caracter_dolor': 'Pulsátil',
            'empeora_actividad': True,
            'nauseas_vomitos': True,
            'fotofobia': True,
            'fonofobia': False,
            'presencia_aura': True,
            'sintomas_aura': 'Visuales, Sensitivos',
            'duracion_aura_minutos': 30,
            'en_menstruacion': False,
            'anticonceptivos': False,
        }

    # 4) Fallback: migraña sin aura por defecto
    return {
        **base,
        'localizacion': 'Unilateral',
        'caracter_dolor': 'Pulsátil',
        'empeora_actividad': True,
        'nauseas_vomitos': True,
        'fotofobia': True,
        'fonofobia': False,
        'presencia_aura': False,
        'sintomas_aura': '',
        'duracion_aura_minutos': 0,
        'en_menstruacion': False,
        'anticonceptivos': False,
    }

def crear_episodio_de_prueba(context, paciente, tipo_migraña):
    """
    Builder de datos de prueba coherente con la categorización (usa repos/servicio FAKE).
    """
    epi_repo = FakeEpisodioCefaleaRepository()
    epi_service = EpisodioCefaleaService(repository=epi_repo)
    datos_episodio = _datos_episodio_por_tipo(tipo_migraña)
    return epi_service.crear_episodio(paciente, datos_episodio)
