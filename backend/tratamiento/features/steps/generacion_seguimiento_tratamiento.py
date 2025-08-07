import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "migraine_app.settings")
django.setup()

from behave import *
from django.utils import timezone
from datetime import datetime, date
from faker import Faker
from tratamiento.repositories import FakeTratamientoRepository
from tratamiento.tratamiento_service import TratamientoService
from tratamiento.models import EpisodioCefalea
from tratamiento.models import Recomendacion

use_step_matcher("re")
fake = Faker('es_ES')

@step("que el paciente tiene al menos un historial de migrañas")
def step_historial_migranas(context):
    inicializar_contexto_basico(context)
    context.tiene_historial = True
    assert context.paciente is not None, "El paciente no fue creado."

@step("que el paciente presenta su primer episodio con la categorización (.+)")
def step_primer_episodio(context, tipo_migrana):
    inicializar_contexto_basico(context)
    context.tipo_migraña_actual = tipo_migrana
    context.primer_episodio = True
    assert context.paciente is not None, "El paciente no fue inicializado."
    assert context.tipo_migraña_actual == tipo_migrana, "El tipo de migraña no coincide."

@step("el médico ingresa los datos del tratamiento")
def step_ingresar_datos(context):
    inicializar_contexto_basico(context)

    context.tratamiento_repository = FakeTratamientoRepository()
    context.tratamiento_service = TratamientoService(context.tratamiento_repository)

    campos_esperados = {'Dosis', 'Medicamento', 'Características', 'Frecuencia', 'Duración tratamiento','Recomendacion'}
    campos_tabla = campos_tabla_ingresar(context)
    assert campos_esperados == campos_tabla, f"Campos faltantes o incorrectos"
    context.campos_tabla = campos_tabla

    context.dosis = fake.random_element(['10', '20', '12', '30'])
    context.medicamento = fake.random_element(['Ibuprofeno', 'Paracetamol', 'Sumatriptán', 'Prednisona'])
    context.duracion_dias = fake.random_element([3, 15, 8])
    context.caracteristica = fake.random_element(['50mg', '500mg', '10mg'])
    context.frecuencia_horas = 8

    context.episodio = crear_episodio_dummy(paciente=context.paciente.usuario, tipo_migraña=context.tipo_migraña_actual)

    context.tratamiento = context.tratamiento_service.crear_tratamiento(
        paciente=context.paciente, episodio=context.episodio, activo=True,
        fecha_inicio=date.today(),
    )

    context.medicamento = context.tratamiento_service.crear_medicamento(
        nombre=context.medicamento,
        dosis=context.dosis,
        caracteristica=context.caracteristica,
        hora_inicio=timezone.now().time(),
        frecuencia_horas=context.frecuencia_horas,
        duracion_dias=context.duracion_dias
    )

    context.tratamiento_service.agregar_medicamento_a_tratamiento(context.tratamiento.id, context.medicamento)

    context.tratamiento.recomendaciones = [Recomendacion.HIDRATACION]
    context.tratamiento_repository.save_tratamiento(context.tratamiento)

    context.tratamiento_creado = context.tratamiento

    assert context.tratamiento_creado is not None, "El tratamiento no fue creado."
    assert context.tratamiento_creado.activo == True, "El tratamiento debe estar activo."


def campos_tabla_ingresar(context):
    campos_tabla = {row['Cantidad'] for row in context.table}
    return campos_tabla


@step("el sistema crea el tratamiento")
def step_crea_tratamiento(context):
    assert hasattr(context, 'tratamiento_creado'), "El tratamiento debió ser creado en el step anterior"
    assert context.tratamiento_creado is not None, "El tratamiento no puede ser None"

    campos_esperados = {'Dosis', 'Medicamento', 'Características', 'Frecuencia', 'Duración tratamiento',
                        'Recomendacion'}
    assert context.campos_tabla == campos_esperados, f"Los campos de la tabla no coinciden con los esperados"

    tratamiento_repositorio = context.tratamiento_repository.get_tratamiento_by_id(context.tratamiento_creado.id)
    context.tratamiento_service.agregar_medicamento_a_tratamiento(context.tratamiento.id, context.medicamento)
    medicamentos_tratamiento = context.tratamiento_repository.get_medicamentos_by_tratamiento_id(context.tratamiento_creado.id)

    assert len(medicamentos_tratamiento) >= 1, "El tratamiento debe tener al menos una medicación"
    assert len(tratamiento_repositorio.recomendaciones) >= 1, "El tratamiento debe tener al menos una recomendación"

    assert context.tratamiento_creado.activo == True, "El tratamiento debe estar activo"
    assert context.tratamiento_creado.estaActivo() == True, "El tratamiento debe estar en estado activo"

    context.tratamiento_generado = context.tratamiento_creado


@step("que el paciente tiene un tratamiento activo correspondiente a un episodio médico")
def step_paciente_con_tratamiento(context):
    inicializar_contexto_basico(context)

    context.tratamiento_repository = FakeTratamientoRepository()
    context.tratamiento_service = TratamientoService(context.tratamiento_repository)

    tipo_migraña = getattr(context, 'tipo_migraña', 'Migraña sin aura')
    context.episodio = crear_episodio_dummy(paciente=context.paciente.usuario, tipo_migraña=tipo_migraña)

    context.tratamiento_activo = context.tratamiento_service.crear_tratamiento(
        paciente=context.paciente,
        episodio=context.episodio,
        fecha_inicio=datetime.now().date(),
        activo=True
    )

    assert context.paciente is not None, "El paciente no fue inicializado."
    assert context.tratamiento_activo.estaActivo(), "El tratamiento no está activo."


@step(
    "el historial de alertas indica que el paciente ha confirmado (?P<porcentaje_cumplimiento>.+)% de las tomas correspondientes a (?P<numero_tratamientos>.+) tratamientos")
def step_historial_cumplimiento(context, porcentaje_cumplimiento, numero_tratamientos):
    inicializar_contexto_basico(context)

    context.tratamiento_repository = FakeTratamientoRepository()
    context.tratamiento_service = TratamientoService(context.tratamiento_repository)

    context.porcentaje_cumplimiento = float(porcentaje_cumplimiento)
    context.cumplimiento_promedio = context.porcentaje_cumplimiento
    context.numero_tratamientos = int(numero_tratamientos)

    context.episodio = crear_episodio_dummy(paciente=context.paciente.usuario, tipo_migraña='Migraña sin aura')
    context.tratamiento_activo = context.tratamiento_service.crear_tratamiento(
        paciente=context.paciente,
        episodio=context.episodio,
        fecha_inicio=datetime.now().date(),
        activo=True
    )
    context.tratamiento_activo.cumplimiento = context.porcentaje_cumplimiento
    context.tratamiento_repository.save_tratamiento(context.tratamiento_activo)
    assert context.tratamiento_activo is not None, "El primer tratamiento debe existir."


@step("el médico evalúa el cumplimiento del tratamiento anterior")
def step_medico_evalua(context):
    tratamiento_1 = context.tratamiento_repository.get_tratamiento_by_id(context.tratamiento_activo.id)

    context.cumplimiento_tratamiento_1 = float(tratamiento_1.cumplimiento)

    context.cumplimiento_tratamiento_1
    context.evaluacion_completada = True

    assert context.cumplimiento_tratamiento_1 >= 0, "El cumplimiento del primer tratamiento debe ser válido."
    assert context.evaluacion_completada == True, "La evaluación debe estar completada."

@step("se decide modificar el tratamiento")
def step_modificar_tratamiento(context):
    context.modificacion_decidida = True
    assert context.modificacion_decidida is True, "La decisión de modificar el tratamiento debe estar tomada"


@step("el médico ingresa las siguientes características para el nuevo tratamiento")
def step_medico_ingresa_caracteristicas(context):
    context.nueva_cantidad = fake.random_element(['10', '20', '12', '30'])
    context.nueva_medicamento = fake.random_element(['Ibuprofeno', 'Paracetamol', 'Sumatriptán'])
    context.nueva_duracion = fake.random_element([3, 15, 8])
    context.caracteristica = fake.random_element(['50mg', '500mg', '10mg'])

    assert context.nueva_cantidad is not None, "La cantidad debe estar definida."
    assert context.nueva_medicamento is not None, "La medicación debe estar definida."


@step("el sistema debe actualizar el tratamiento con los nuevos datos")
def step_sistema_actualiza(context):

    nuevo_medicamento = context.tratamiento_service.crear_medicamento(
        nombre=context.nueva_medicamento,
        dosis=context.nueva_cantidad,
        caracteristica=context.caracteristica,
        hora_inicio=datetime.now().time(),
        frecuencia_horas=8,
        duracion_dias=context.nueva_duracion
    )

    context.tratamiento_service.agregar_medicamento_a_tratamiento(
        context.tratamiento_activo.id,
        nuevo_medicamento
    )

    context.tratamiento_repository.save_tratamiento(context.tratamiento_activo)
    context.actualizacion_exitosa = True

    assert context.actualizacion_exitosa == True, "La actualización debe ser exitosa."


@step('se decide cancelar el tratamiento')
def step_cancelar_tratamiento_actual(context):
    assert context.cumplimiento_promedio < 80, f"El cumplimiento promedio debe ser menor a 80%"
    context.decision_cancelacion = True

@step('el médico ingresa el motivo como "(?P<motivo_cancelacion>.+)"')
def step_ingresar_motivo(context, motivo_cancelacion):
    context.motivo_cancelacion = motivo_cancelacion
    assert len(motivo_cancelacion.strip()) > 0, "El motivo no puede estar vacío"


@step("el sistema debe cancelar el tratamiento con los datos ingresados")
def step_cancelar_tratamiento(context):
    tratamiento_a_cancelar = context.tratamiento_repository.get_tratamiento_by_id(context.tratamiento_activo.id)
    tratamiento_a_cancelar.activo = False
    tratamiento_a_cancelar.motivo_cancelacion = context.motivo_cancelacion

    context.tratamiento_repository.save_tratamiento(tratamiento_a_cancelar)

    context.tratamiento_cancelado = tratamiento_a_cancelar
    context.cancelacion_realizada = True

    assert tratamiento_a_cancelar.activo is False, "El tratamiento debe estar inactivo"
    assert context.cancelacion_realizada == True, "La cancelación debe estar realizada"


def inicializar_contexto_basico(context):
    """
       Inicializa el contexto básico usando FakeUserRepository
       en lugar de la base de datos real
       """
    from usuarios.repositories import FakeUserRepository
    from faker import Faker
    from datetime import date
    import random

    fake = Faker('es_ES')  # Para datos en español

    # Crear instancia del repositorio fake
    context.fake_repo = FakeUserRepository()

    # Crear usuario paciente usando el repositorio fake
    user_data_paciente = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'cedula': str(fake.unique.random_number(digits=10, fix_len=True)),
        'telefono': fake.msisdn()[3:13],  # Generar teléfono de 10 dígitos
        'fecha_nacimiento': fake.date_of_birth(minimum_age=18, maximum_age=80),
        'genero': fake.random_element(['M', 'F', 'O', 'N']),
        'direccion': fake.address(),
    }

    profile_data_paciente = {
        'grupo_sanguineo': fake.random_element(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
        'contacto_emergencia_nombre': fake.name(),
        'contacto_emergencia_telefono': fake.msisdn()[3:13],  # Teléfono de 10 dígitos
        'contacto_emergencia_relacion': fake.random_element(
            ['Padre', 'Madre', 'Hermano', 'Hermana', 'Cónyuge', 'Hijo', 'Hija'])
    }

    # Crear paciente usando el repositorio
    context.usuario_paciente = context.fake_repo.create_paciente(user_data_paciente, profile_data_paciente)

    # Obtener el perfil del paciente creado
    context.paciente = next(
        (p for p in context.fake_repo.get_all_pacientes() if p.usuario.id == context.usuario_paciente.id),
        None
    )

    # Crear usuario médico usando el repositorio fake
    user_data_medico = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.unique.email(),
        'cedula': str(fake.unique.random_number(digits=10, fix_len=True)),
        'telefono': fake.msisdn()[3:13],  # Generar teléfono de 10 dígitos
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

    # Crear médico usando el repositorio
    context.usuario_medico = context.fake_repo.create_medico(user_data_medico, profile_data_medico)

    # Obtener el perfil del médico creado
    context.medico = next(
        (m for m in context.fake_repo.get_all_medicos() if m.usuario.id == context.usuario_medico.id),
        None
    )

def crear_episodio_dummy(paciente, tipo_migraña):
    """
    Crear episodio dummy específicamente para BDD testing.
    Siempre usa repositorio fake.
    """
    from evaluacion_diagnostico.repositories import FakeEpisodioCefaleaRepository
    from evaluacion_diagnostico.episodio_cefalea_service import EpisodioCefaleaService

    # Servicio with fake repository
    repository = FakeEpisodioCefaleaRepository()
    episodio_service = EpisodioCefaleaService(repository=repository)

    # Datos del episodio
    datos_episodio = {
        'duracion_cefalea_horas': 2,
        'severidad': 'Moderada',
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
        'categoria_diagnostica': tipo_migraña
    }

    return episodio_service.crear_episodio(paciente, datos_episodio)

