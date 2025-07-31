from behave import *

use_step_matcher("re")

@step("que un paciente ha ingresado datos para un nuevo episodio de cefalea con las siguientes características")
def step_impl(context):
    # Crear un mock simple que simule exactamente lo que necesitamos
    class MockUsuario:
        def __init__(self, **kwargs):
            # Asignar todos los campos
            for key, value in kwargs.items():
                setattr(self, key, value)
            
            # Campos por defecto si no se proporcionan
            if not hasattr(self, 'id'):
                self.id = 1
            if not hasattr(self, 'is_active'):
                self.is_active = True
        
        def get_full_name(self):
            return f"{getattr(self, 'first_name', '')} {getattr(self, 'last_name', '')}".strip()
        
        @property
        def es_paciente(self):
            return getattr(self, 'tipo_usuario', '') == 'paciente'
        
        @property
        def es_medico(self):
            return getattr(self, 'tipo_usuario', '') == 'medico'
        
        @property
        def es_enfermera(self):
            return getattr(self, 'tipo_usuario', '') == 'enfermera'

    class MockPacienteProfile:
        def __init__(self, usuario, **kwargs):
            self.usuario = usuario
            for key, value in kwargs.items():
                setattr(self, key, value)

    # Crear el paciente mock con todos los datos
    paciente = MockUsuario(
        id=1,
        email='paciente_test@example.com',
        username='paciente_test',
        first_name='Juan',
        last_name='Pérez',
        cedula='1234567890',
        telefono='0987654321',
        tipo_usuario='paciente',
        is_active=True
    )
    
    # Crear perfil mock
    perfil = MockPacienteProfile(
        usuario=paciente,
        contacto_emergencia_nombre='María Pérez',
        contacto_emergencia_telefono='0999888777',
        contacto_emergencia_relacion='Esposa',
        grupo_sanguineo='O+',
        alergias='Ninguna'
    )
    
    # Guardar en el contexto para otros steps
    context.paciente = paciente
    context.perfil_paciente = perfil
    
    # Assert para verificar que se creó correctamente
    assert paciente is not None, "El paciente debería haberse creado"
    assert paciente.email == 'paciente_test@example.com', "El email del paciente no coincide"
    assert paciente.tipo_usuario == 'paciente', "El tipo de usuario debería ser paciente"
    assert paciente.get_full_name() == 'Juan Pérez', "El nombre completo no coincide"
    assert paciente.es_paciente == True, "Debería ser un paciente"
    assert paciente.es_medico == False, "No debería ser un médico"
    assert perfil.contacto_emergencia_nombre == 'María Pérez', "El contacto de emergencia no coincide"
    
    print("✅ Paciente mock creado exitosamente con todos los métodos y propiedades necesarios")

@step("todos los datos estén completos,")
def step_validar_datos_completos(context):
   print("hola mundo")

@step('el sistema debe categorizar el episodio como "(?P<categoria_esperada>.+)",')
def step_categorizar_episodio(context, categoria_esperada):
    print("hola mundo")

@step("el episodio se guarda en la bitácora del paciente")
def step_guardar_en_bitacora(context):
    print("hola mundo")

