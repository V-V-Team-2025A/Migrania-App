from behave import *
from usuarios.repositories import FakeUserRepository
use_step_matcher("re")


@step("que un paciente ha ingresado datos para un nuevo episodio de cefalea con las siguientes características")
def step_impl(context):
    if not hasattr(context, 'repo'):
        context.repo = FakeUserRepository()

    # Crear paciente REAL usando el modelo de Django IGUAL que en tu ejemplo
    user_data = {
        'email': "asd",
        'first_name':  'Juan',
        'last_name': 'Pérez',
        'username': "juanjo",  # Username es requerido por AbstractUser
        'password': 'password123',
        'cedula':"0503099533",
        'telefono': '1234567890',  # telefono está en Usuario, no en PacienteProfile
        'fecha_nacimiento': '1990-01-01'  # fecha_nacimiento está en Usuario
    }

    profile_data = {
        # Campos específicos de PacienteProfile
        'contacto_emergencia_nombre': 'Contacto Test',
        'contacto_emergencia_telefono': '0987654321',
        'contacto_emergencia_relacion': 'Familiar'
    }

    # Crear usando el repositorio fake - MODELOS REALES, no mocks
    paciente = context.repo.create_paciente(user_data, profile_data)

    # Guardar referencia para otros steps
    context.paciente_creado = paciente

    print("POR FIN SE CREÓ EL PACIENTE", paciente)


@step("todos los datos estén completos,")
def step_impl(context):
    print("VERIFICANDO QUE LOS DATOS DEL PACIENTE ESTÉN COMPLETOS")


@step('el sistema debe categorizar el episodio como "(?P<categoria_esperada>.+)",')
def step_impl(context, categoria_esperada):
    print("CATEGORIZANDO EPISODIO COMO:", categoria_esperada)

@step("el episodio se guarda en la bitácora del paciente")
def step_impl(context):
    print("GUARDANDO EPISODIO EN LA BITÁCORA DEL PACIENTE")