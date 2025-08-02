# evaluacion_diagnostico/features/steps/bitacora_digital_step.py

from behave import *
from usuarios.repositories import FakeUserRepository
from evaluacion_diagnostico.repositories import FakeEpisodioCefaleaRepository
from evaluacion_diagnostico.episodio_cefalea_service import EpisodioCefaleaService
from django.core.exceptions import ValidationError

# Usar el comparador de expresiones regulares para los steps
use_step_matcher("re")


@given("que un paciente ha ingresado datos para un nuevo episodio de cefalea con las siguientes características")
def step_impl(context):
    # 1. Preparar repositorios en memoria para una prueba aislada
    user_repo = FakeUserRepository()
    episode_repo = FakeEpisodioCefaleaRepository()

    # 2. Inyectar el repositorio FAKE en el servicio para desacoplar la lógica
    context.episodio_service = EpisodioCefaleaService(repository=episode_repo)

    # 3. Crear un paciente de prueba para asociar el episodio.
    user_data = {
        'username': "joanitoRosa",
        'email': "paciente@test.com",
        'password': 'testpassword',
        'first_name': 'Juanito',
        'last_name': 'Del Rosario'
    }
    # Aunque no necesitemos datos de perfil para esta prueba, el método espera el diccionario.
    profile_data = {
        'contacto_emergencia_nombre': 'Juanita Burbano',
        'contacto_emergencia_telefono': '0992675567',
        'contacto_emergencia_relacion': '0992673389'
    }

    context.paciente = user_repo.create_paciente(user_data, profile_data)

    # 4. Procesar los datos de la tabla del feature y guardarlos en el contexto
    datos_tabla = {row['Característica']: row['Valor'] for row in context.table}
    context.datos_episodio_procesados = context.episodio_service.procesar_datos_episodio(datos_tabla)

    # 5. Guardar el repositorio en el contexto para usarlo en el último 'Then'
    context.episode_repo = episode_repo


@when("todos los datos estén completos,")
def step_impl(context):
    try:
        context.episodio_creado = context.episodio_service.crear_episodio(
            paciente=context.paciente,
            datos_episodio=context.datos_episodio_procesados
        )
        context.error = None
    except ValidationError as e:
        context.episodio_creado = None
        context.error = e


@then('el sistema debe categorizar el episodio como "(?P<categoria_esperada>.+)",')
def step_impl(context, categoria_esperada):
    assert context.episodio_creado is not None, "El episodio no fue creado, se encontró un error."

    assert context.episodio_creado.categoria_diagnostica == categoria_esperada, \
        f"Se esperaba la categoría '{categoria_esperada}', pero se obtuvo '{context.episodio_creado.categoria_diagnostica}'"


@then("el episodio se guarda en la bitácora del paciente")
def step_impl(context):

    ultimo_episodio_guardado = context.episode_repo.obtener_ultimo_episodio(context.paciente)

    assert ultimo_episodio_guardado is not None, "El episodio no se guardó en la bitácora del paciente."

    assert ultimo_episodio_guardado.pk == context.episodio_creado.pk, \
        "El episodio guardado en la bitácora no es el que se acaba de crear."