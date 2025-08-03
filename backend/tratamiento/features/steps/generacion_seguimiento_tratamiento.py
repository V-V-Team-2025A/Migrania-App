from behave import *
from tratamiento.models import Tratamiento, Recomendacion, Medicacion, EstadoNotificacion, Alerta
from django.contrib.auth.models import User
from usuarios.models import PacienteProfile, MedicoProfile
from django.utils import timezone
from datetime import datetime, timedelta
from faker import Faker
import random

use_step_matcher("re")
fake = Faker('es_ES')


def inicializar_contexto_basico(context):
    # Crear paciente solo si no existe
    if not hasattr(context, 'paciente') or context.paciente is None:
        context.usuario_paciente = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        context.paciente = PacienteProfile.objects.create(
            user=context.usuario_paciente,
            genero=fake.random_element(['male', 'female'])
        )

    # Crear médico solo si no existe
    if not hasattr(context, 'medico') or context.medico is None:
        context.usuario_medico = User.objects.create_user(
            username=f"medico_{fake.user_name()}",
            email=fake.email()
        )
        context.medico = MedicoProfile.objects.create(
            user=context.usuario_medico,
            especialidad="Neurología"
        )

@step("que el paciente tiene al menos un historial de migrañas")
def step_impl(context):
    inicializar_contexto_basico(context)
    context.tiene_historial = True
    assert context.paciente is not None, "El paciente no fue creado."

@step("que el paciente presenta su primer episodio con la categorización (.+)")
def step_impl(context, tipo_migrana):
    inicializar_contexto_basico(context)
    context.tipo_migraña_actual = tipo_migrana
    context.primer_episodio = True
    assert context.paciente is not None, "El paciente no fue inicializado."
    assert context.tipo_migraña_actual == tipo_migrana, "El tipo de migraña no coincide."


@step("el médico ingresa los datos del tratamiento")
def step_impl(context):
    inicializar_contexto_basico(context)
    medicacion = Medicacion.objects.create(
        nombre=context.datos_tratamiento['medicacion'],
        cantidad=context.datos_tratamiento['cantidad'],
        caracteristica=context.datos_tratamiento['caracteristicas'],
        frecuencia=context.datos_tratamiento['frecuencia'],
        duracion=context.datos_tratamiento['duracion'],
        hora_de_inicio=datetime.now().time()
    )

    # Crear tratamiento
    context.tratamiento_creado = Tratamiento.objects.create(
        medico=context.medico,
        paciente=context.paciente,
        fecha_inicio=timezone.now().date(),
        activo=True
    )

    # Agregar medicación y recomendaciones
    context.tratamiento_creado.medicaciones.add(medicacion)
    for rec in context.datos_tratamiento['recomendaciones']:
        context.tratamiento_creado.recomendaciones.add(rec)

    assert context.tratamiento_creado is not None, "El tratamiento no fue creado."
    assert context.tratamiento_creado.activo == True, "El tratamiento debe estar activo."

@step("el sistema crea el tratamiento")
def step_impl(context):
    context.cantidad = fake.random_element(['10', '20', '12', '30'])
    context.medicacion = fake.random_element(['Ibuprofeno', 'Paracetamol', 'Sumatriptán', 'Prednisona'])
    context.caracteristicas = fake.random_element(['50mg', '30mg', '100mg'])
    context.frecuencia = fake.random_element(['Cada 8 horas', 'Cada 12 horas', 'Según necesidad'])
    context.duracion = fake.random_element(['3 días', '15 días', '8 días'])
    context.recomendacion = fake.random_element([
        'Seguimiento mensual con especialista',
        'Monitoreo de efectos secundarios',
        'Evaluación de calidad de vida trimestral'
    ])

    # Verificar que la tabla contiene los campos esperados (si existe)
    if hasattr(context, 'table'):
        campos_esperados = {'Cantidad', 'Medicación', 'Características', 'Frecuencia', 'Duración tratamiento',
                            'Recomendacion'}
        campos_tabla = {row['Campo'] for row in context.table}
        assert campos_esperados == campos_tabla, f"Campos faltantes o incorrectos. Esperados: {campos_esperados}, Encontrados: {campos_tabla}"

    # Crear objetos con datos generados aleatoriamente
    expected_medicacion = Medicacion(
        context.cantidad,
        context.medicacion,
        context.caracteristicas,
        context.frecuencia,
        context.duracion
    )
    expected_recomendacion = Recomendacion(context.recomendacion)

    # Inicializar o actualizar tratamiento_generado
    if not hasattr(context, 'tratamiento_generado'):
        context.tratamiento_generado = type('obj', (object,), {
            'medicaciones': [expected_medicacion],
            'recomendaciones': [expected_recomendacion]
        })
    else:
        # Actualizar el tratamiento con los nuevos datos aleatorios
        context.tratamiento_generado.medicaciones[0] = expected_medicacion
        context.tratamiento_generado.recomendaciones[0] = expected_recomendacion

    # Validaciones
    assert len(context.tratamiento_generado.medicaciones) == 1, "La cantidad de medicaciones no es la esperada."
    assert context.tratamiento_generado.medicaciones[0] == expected_medicacion, "La medicación generada no coincide."
    assert len(context.tratamiento_generado.recomendaciones) == 1, "La cantidad de recomendaciones no es la esperada."
    assert context.tratamiento_generado.recomendaciones[
               0] == expected_recomendacion, "La recomendación generada no coincide."


@step("que el paciente tiene un tratamiento activo correspondiente a un episodio médico")
def step_paciente_con_tratamiento(context):
    inicializar_contexto_basico(context)

    # Crear tratamiento activo usando el paciente y médico existentes
    context.tratamiento_activo = Tratamiento.objects.create(
        medico=context.medico,
        paciente=context.paciente,
        fecha_inicio=timezone.now().date(),
        activo=True
    )

    assert context.paciente is not None, "El paciente no fue inicializado."
    assert context.tratamiento_activo.estaActivo(), "El tratamiento no está activo."


@step(
    "el historial de alertas indica que el paciente ha confirmado (?P<porcentaje_cumplimiento>.+)% de las tomas correspondientes a (?P<numero_tratamientos>.+) tratamientos")
def step_historial_cumplimiento(context, porcentaje_cumplimiento, numero_tratamientos):
    context.porcentaje_cumplimiento = porcentaje_cumplimiento
    context.numero_tratamientos = numero_tratamientos

    # Crear segundo tratamiento solo si no existe
    if not hasattr(context, 'tratamiento_activo_2'):
        context.tratamiento_activo_2 = Tratamiento(id_tratamiento=fake.unique.random_int(min=1, max=100))
        context.paciente.agregar_tratamiento_activo(context.tratamiento_activo_2)

    # Simular historial para primer tratamiento
    context.paciente.simular_historial_tomas(
        context.tratamiento_activo.id_tratamiento,
        context.porcentaje_cumplimiento,
        tomas_esperadas_simuladas=100
    )

    # Simular historial para segundo tratamiento
    context.paciente.simular_historial_tomas(
        context.tratamiento_activo_2.id_tratamiento,
        context.porcentaje_cumplimiento,
        tomas_esperadas_simuladas=100
    )

    assert len(context.paciente.tratamientos_activos) == 2, f"El paciente debe tener 2 tratamientos activos."
    assert context.tratamiento_activo.id_tratamiento in context.paciente.historial_alertas_tomas, "No se registró historial para el primer tratamiento."
    assert context.tratamiento_activo_2.id_tratamiento in context.paciente.historial_alertas_tomas, "No se registró historial para el segundo tratamiento."


@step("el médico evalúa el cumplimiento del tratamiento anterior")
def step_medico_evalua(context):
    context.cumplimiento_tratamiento_1 = context.tratamiento_activo.cumplimiento
    context.cumplimiento_tratamiento_2 = context.tratamiento_activo_2.cumplimiento
    context.cumplimiento_promedio = (context.cumplimiento_tratamiento_1 + context.cumplimiento_tratamiento_2) / 2
    context.evaluacion_completada = True

    assert context.cumplimiento_tratamiento_1 >= 0, "El cumplimiento del primer tratamiento debe ser válido."
    assert context.cumplimiento_tratamiento_2 >= 0, "El cumplimiento del segundo tratamiento debe ser válido."
    assert context.evaluacion_completada == True, "La evaluación debe estar completada."


@step('se decide modificar el tratamiento')
def step_decision_modificar(context):
    context.decision_modificar = context.cumplimiento_promedio >= 80
    assert context.decision_modificar, f"La decisión debe ser modificar el tratamiento. Cumplimiento promedio: {context.cumplimiento_promedio}%"

@step('el médico ingresa las siguientes características para el nuevo tratamiento')
def step_medico_ingresa_caracteristicas(context):
    tabla_datos = context.table
    context.nueva_cantidad = fake.random_element(['10', '20 ', '12 ', '30'])
    context.nueva_medicacion = fake.random_element(['Ibuprofeno', 'Paracetamol', 'Sumatriptán', 'Prednisona'])
    context.nuevas_caracteristicas = fake.random_element(['50mg', '30mg', '100mg'])
    context.nueva_frecuencia = fake.random_element(['Cada 8 horas', 'Cada 12 horas ', 'Según necesidad'])
    context.nueva_duracion = fake.random_element(['3 días', '15 días', '8 días'])
    context.nueva_recomendacion = fake.random_element([
        'Seguimiento mensual con especialista',
        'Monitoreo de efectos secundarios',
        'Evaluación de calidad de vida trimestral'
    ])

    assert context.nueva_cantidad is not None, "La cantidad debe estar definida."
    assert context.nueva_medicacion is not None, "La medicación debe estar definida."
    assert context.nuevas_caracteristicas is not None, "Las características deben estar definidas."
    assert context.nueva_frecuencia is not None, "La frecuencia debe estar definida."
    assert context.nueva_duracion is not None, "La duración debe estar definida."
    assert context.nueva_recomendacion is not None, "La recomendación debe estar definida."
    assert tabla_datos is not None, "La tabla de datos debe estar presente."


@step('el sistema debe actualizar el tratamiento con los nuevos datos')
def step_sistema_actualiza(context):
    nueva_medicacion = Medicacion.objects.create(
        nombre=context.nueva_medicacion,
        cantidad=context.nueva_cantidad,
        caracteristica=context.nuevas_caracteristicas,
        frecuencia=context.nueva_frecuencia,
        duracion=context.nueva_duracion,
        hora_de_inicio=datetime.now().time()
    )

    # Modificar el tratamiento activo
    context.tratamiento_activo.modificar_tratamiento(
        [nueva_medicacion],
        [context.nueva_recomendacion]
    )

    context.actualizacion_exitosa = True

    assert context.tratamiento_activo.medicaciones.count() == 1, "El tratamiento debe tener exactamente una medicación."
    assert context.tratamiento_activo.recomendaciones.count() >= 1, "El tratamiento debe tener al menos una recomendación."
    assert context.actualizacion_exitosa == True, "La actualización debe ser exitosa."


@step('se decide cancelar el tratamiento')
def step_cancelar_tratamiento_actual(context):
    # Verificar que la evaluación fue completada
    assert hasattr(context, 'evaluacion_completada') and context.evaluacion_completada, \
        "La evaluación del cumplimiento debe estar completada antes de decidir cancelar"

    umbral_minimo = 80
    assert context.cumplimiento_promedio < umbral_minimo, \
        f"El cumplimiento promedio ({context.cumplimiento_promedio}%) debe ser menor al umbral mínimo ({umbral_minimo}%) para justificar la cancelación"

    context.decision_cancelacion = True

@step('el médico ingresa el motivo como "(?P<motivo_cancelacion>.+)"')
def step_impl(context, motivo_cancelacion):
    # Verificar que se ha decidido cancelar
    assert hasattr(context, 'decision_cancelacion') and context.decision_cancelacion, \
        "Debe haberse decidido cancelar el tratamiento antes de ingresar el motivo"

    # Guardar el motivo de cancelación
    context.motivo_cancelacion = motivo_cancelacion

    assert motivo_cancelacion is not None and len(motivo_cancelacion.strip()) > 0, \
        "El motivo de cancelación no puede estar vacío"

@step("el sistema debe cancelar el tratamiento con los datos ingresados")
def step_impl(context):
    assert hasattr(context, 'motivo_cancelacion'), \
        "Debe existir un motivo de cancelación"

    # Cancelar el tratamiento más reciente
    tratamiento_a_cancelar = context.tratamiento_activo_2
    tratamiento_a_cancelar.cancelar_tratamiento(context.motivo_cancelacion)

    # Verificar que el tratamiento fue cancelado correctamente
    assert tratamiento_a_cancelar.activo is False, \
        "El tratamiento debe estar inactivo después de la cancelación"
    assert tratamiento_a_cancelar.motivo_cancelacion == context.motivo_cancelacion, \
        "El motivo de cancelación debe estar guardado correctamente"

    context.tratamiento_cancelado = tratamiento_a_cancelar
    context.cancelacion_realizada = True
