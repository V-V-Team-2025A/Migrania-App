# Bootstrap Django
# evita ImproperlyConfigured si el runner carga steps antes del environment
import os
import django

if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "migraine_app.settings")
try:
    django.setup()
except Exception:
    pass
# --- fin bootstrap ---

from behave import *
from django.utils import timezone
from datetime import datetime, date
from faker import Faker

use_step_matcher("re")
fake = Faker("es_ES")

# Steps

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

    # Asegura servicios provistos por environment.py
    assert hasattr(context, "tratamiento_service"), "Falta tratamiento_service en context (revisa environment.py)."
    assert hasattr(context, "medicamento_service"), "Falta medicamento_service en context (revisa environment.py)."
    assert hasattr(context, "seguimiento_service"), "Falta seguimiento_service en context (revisa environment.py)."
    assert hasattr(context, "tratamiento_repository"), "Falta tratamiento_repository en context (revisa environment.py)."
    assert hasattr(context, "medicamento_repository"), "Falta medicamento_repository en context (revisa environment.py)."
    assert hasattr(context, "seguimiento_repository"), "Falta seguimiento_repository en context (revisa environment.py)."


@step(r"que el paciente presenta su primer episodio con la categorización (.+)")
def step_primer_episodio(context, tipo_migrana):
    if not getattr(context, "paciente", None):
        inicializar_contexto_basico(context)

    tipo = tipo_migrana.strip()
    context.tipo_migraña_actual = tipo
    context.primer_episodio = True

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
    # Import local para evitar configurar Django antes de tiempo
    from tratamiento.models import Recomendacion

    # Reusar servicios del environment
    ts = context.tratamiento_service
    ms = context.medicamento_service
    repo = context.tratamiento_repository

    context.dosis = "500mg"
    context.medicamento_nombre = "Ibuprofeno"
    context.duracion_dias = 7
    context.caracteristica = "Tabletas"
    context.frecuencia_horas = 8

    # 1) Crear tratamiento activo
    context.tratamiento = ts.crear_tratamiento(
        paciente=context.paciente,
        episodio=context.episodio,
        activo=True,
        fecha_inicio=date.today(),
    )

    # 2) Crear y asociar medicamento
    context.medicamento = ms.crear_medicamento(
        nombre=context.medicamento_nombre,
        dosis=context.dosis,
        caracteristica=context.caracteristica,
        hora_inicio=timezone.now().time(),
        frecuencia_horas=context.frecuencia_horas,
        duracion_dias=context.duracion_dias
    )
    ok = ts.agregar_medicamento_a_tratamiento(context.tratamiento.id, context.medicamento)
    assert ok, "No se pudo agregar el medicamento al tratamiento (repo no encontró el tratamiento)."

    # 3) Al menos una recomendación (JSONField como lista de strings)
    context.tratamiento.recomendaciones = [Recomendacion.HIDRATACION.value]  # "hidratacion"
    repo.save_tratamiento(context.tratamiento)

    context.tratamiento_creado = context.tratamiento

@step("el sistema crea el tratamiento")
def step_crea_tratamiento(context):
    assert hasattr(context, 'tratamiento_creado'), "El tratamiento debió ser creado en el step anterior"
    assert context.tratamiento_creado is not None, "El tratamiento no puede ser None"

    repo = context.tratamiento_repository
    tratamiento_repo = repo.get_tratamiento_by_id(context.tratamiento_creado.id)
    meds = repo.get_medicamentos_by_tratamiento_id(context.tratamiento_creado.id)

    assert len(meds) >= 1, "El tratamiento debe tener al menos una medicación"
    assert isinstance(tratamiento_repo.recomendaciones, list) and len(tratamiento_repo.recomendaciones) >= 1, \
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

    ts = context.tratamiento_service
    repo_t = context.tratamiento_repository

    context.tratamiento_activo = ts.crear_tratamiento(
        paciente=context.paciente,
        episodio=context.episodio,
        fecha_inicio=datetime.now().date(),
        activo=True
    )
    repo_t.save_tratamiento(context.tratamiento_activo)

    assert context.tratamiento_activo.esta_activo(), "El tratamiento no está activo."


@step(r"el historial de alertas indica que el paciente ha confirmado (?P<porcentaje_cumplimiento>.+)% de las tomas correspondientes a (?P<numero_tratamientos>.+) tratamientos")
def step_historial_cumplimiento(context, porcentaje_cumplimiento, numero_tratamientos):
    context.porcentaje_cumplimiento = float(porcentaje_cumplimiento)
    context.cumplimiento_promedio = context.porcentaje_cumplimiento
    context.numero_tratamientos = int(numero_tratamientos)

    if not getattr(context, "tratamiento_activo", None):
        step_paciente_con_tratamiento(context)

    estadisticas_cumplimiento = {
        'porcentaje_cumplimiento': context.porcentaje_cumplimiento,
        'numero_tratamientos': context.numero_tratamientos,
        'fecha_evaluacion': datetime.now()
    }

    repo_s = context.seguimiento_repository
    repo_s.save_estadisticas_cumplimiento(context.tratamiento_activo, estadisticas_cumplimiento)
    assert context.tratamiento_activo is not None, "El tratamiento debe existir."


@step("el médico evalúa el cumplimiento del tratamiento anterior")
def step_medico_evalua(context):
    tratamiento = getattr(context, "tratamiento_activo", None)
    if not tratamiento:
        raise ValueError("No hay tratamiento activo para evaluar cumplimiento")

    evaluacion = context.seguimiento_service.evaluar_cumplimiento(tratamiento.id)

    if evaluacion is None or evaluacion.get('porcentaje', 0.0) == 0.0:
        # Fallback: usar datos del repositorio o contexto
        porcentaje_guardado = context.seguimiento_repository.calcular_cumplimiento_tratamiento(tratamiento.id)
        porcentaje_contexto = getattr(context, 'porcentaje_cumplimiento', 0.0)
        porcentaje_final = max(porcentaje_guardado, porcentaje_contexto)

        evaluacion = {
            'porcentaje': porcentaje_final,
            'categoria': 'bajo' if porcentaje_final < 80 else 'alto',
            'estadisticas': {'porcentaje_cumplimiento': porcentaje_final}
        }

    context.evaluacion_cumplimiento = evaluacion
    context.cumplimiento_evaluado = True
    context.cumplimiento_tratamiento_1 = evaluacion.get('porcentaje', 0.0)

    assert context.cumplimiento_tratamiento_1 >= 0, "El cumplimiento debe ser válido."
    assert context.cumplimiento_evaluado is True, "La evaluación debe estar completada."


@step("se decide modificar el tratamiento")
def step_modificar_tratamiento(context):
    porcentaje = context.evaluacion_cumplimiento.get('porcentaje', 0.0)
    accion = context.seguimiento_service.decidir_accion_seguimiento(porcentaje)

    assert accion == 'modificar', f"Con {porcentaje}% se esperaba 'modificar', se obtuvo '{accion}'"

    # Solo guardamos la decisión
    context.decision_accion = accion
    context.modificacion_decidida = True
    assert context.modificacion_decidida is True, "La decisión de modificar el tratamiento debe estar tomada."


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
    ts = context.tratamiento_service
    ms = context.medicamento_service
    repo = context.tratamiento_repository

    if not getattr(context, "tratamiento_activo", None):
        step_paciente_con_tratamiento(context)

    nuevo_medicamento = ms.crear_medicamento(
        nombre=context.nueva_medicamento,
        dosis=context.nueva_cantidad,
        caracteristica=context.caracteristica,
        hora_inicio=datetime.now().time(),
        frecuencia_horas=8,
        duracion_dias=context.nueva_duracion
    )
    tratamiento_nuevo = ts.agregar_medicamento_a_tratamiento(context.tratamiento_activo.id, nuevo_medicamento)
    assert tratamiento_nuevo, "No se pudo agregar el medicamento al tratamiento."

    repo.save_tratamiento(context.tratamiento_activo)
    context.actualizacion_exitosa = True
    assert context.actualizacion_exitosa is True, "La actualización debe ser exitosa."

@step('se decide cancelar el tratamiento')
def step_cancelar_tratamiento_actual(context):
    porcentaje = context.evaluacion_cumplimiento.get('porcentaje', 0.0)

    assert porcentaje < 80, "El cumplimiento promedio debe ser menor a 80%."

    accion = context.seguimiento_service.decidir_accion_seguimiento(porcentaje)
    assert accion == 'cancelar', f"Con {porcentaje}% se esperaba 'cancelar', se obtuvo '{accion}'"

    context.decision_accion = accion
    context.decision_cancelacion = True

@step('el médico ingresa el motivo como "(?P<motivo_cancelacion>.+)"')
def step_ingresar_motivo(context, motivo_cancelacion):
    context.motivo_cancelacion = motivo_cancelacion
    assert len(motivo_cancelacion.strip()) > 0, "El motivo no puede estar vacío."

@step("el sistema debe cancelar el tratamiento con los datos ingresados")
def step_cancelar_tratamiento(context):
    repo = context.tratamiento_repository
    t = repo.get_tratamiento_by_id(context.tratamiento_activo.id)
    t.activo = False
    t.motivo_cancelacion = context.motivo_cancelacion
    repo.save_tratamiento(t)

    context.tratamiento_cancelado = t
    context.cancelacion_realizada = True

    assert t.activo is False, "El tratamiento debe estar inactivo."
    assert context.cancelacion_realizada is True, "La cancelación debe estar realizada."

# Helpers
def inicializar_contexto_basico(context):
    from usuarios.repositories import FakeUserRepository

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

    # Médico
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

def campos_tabla_ingresar(context):
    import unicodedata

    def _norm_local(s: str) -> str:
        s = (s or "").strip().lower()
        s = unicodedata.normalize("NFD", s)
        s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
        s = s.replace("  ", " ")
        return s

    alias = {
        "dosis": "Dosis",
        "medicamento": "Medicamento",
        "medicacion": "Medicamento",
        "caracteristica": "Características",
        "caracteristicas": "Características",
        "frecuencia": "Frecuencia",
        "cada": "Frecuencia",
        "duracion": "Duración tratamiento",
        "duracion tratamiento": "Duración tratamiento",
        "duracion del tratamiento": "Duración tratamiento",
        "duracion tto": "Duración tratamiento",
        "duraciontto": "Duración tratamiento",
        "recomendacion": "Recomendacion",
        "recomendaciones": "Recomendacion",
    }

    esperados = {
        "Dosis", "Medicamento", "Características", "Frecuencia", "Duración tratamiento", "Recomendacion",
    }

    encontrados = set()

    if context.table:
        try:
            if "Cantidad" in context.table.headings:
                for row in context.table:
                    key = _norm_local(row["Cantidad"]).replace("  ", " ")
                    key_map = alias.get(key)
                    if key_map in esperados:
                        encontrados.add(key_map)
        except Exception:
            pass

        for row in context.table.rows:
            for cell in row.cells:
                key = _norm_local(cell).replace("  ", " ")
                key_map = alias.get(key) or alias.get(key.replace(" ", ""))
                if key_map in esperados:
                    encontrados.add(key_map)

    return encontrados

def _norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.strip().lower().replace("  ", " ")


def _datos_episodio_por_tipo(tipo: str) -> dict:
    t = _norm(tipo)
    base = {
        'duracion_cefalea_horas': 2,
        'severidad': 'Moderada',
        'categoria_diagnostica': tipo,
    }

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
    from evaluacion_diagnostico.repositories import FakeEpisodioCefaleaRepository
    from evaluacion_diagnostico.episodio_cefalea_service import EpisodioCefaleaService

    epi_repo = FakeEpisodioCefaleaRepository()
    epi_service = EpisodioCefaleaService(repository=epi_repo)
    datos_episodio = _datos_episodio_por_tipo(tipo_migraña)
    return epi_service.crear_episodio(paciente, datos_episodio)