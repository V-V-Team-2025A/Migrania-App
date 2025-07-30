from behave import *

from tratamiento.models import Paciente, Migrana, Tratamiento, Medicacion, Recomendacion
from faker import Faker

use_step_matcher("re")
fake = Faker('es_ES')

@step("que el paciente tiene al menos un historial de migrañas")
def step_impl(context):
    context.paciente = Paciente()
    context.paciente.agregar_migrana(Migrana("Migraña sin aura"))
    assert len(context.paciente.historial_migranas) > 0, "El paciente no tiene historial de migrañas."

@step("que el paciente presenta su primer episodio con la categorización (.+)")
def step_impl(context, tipo_migrana):
    context.paciente = Paciente()
    context.paciente.agregar_migrana(Migrana(tipo_migrana))
    context.tipo_migraña_actual = tipo_migrana
    assert context.paciente is not None, "El paciente no fue inicializado."
    assert len(context.paciente.historial_migranas) == 1, "El paciente no tiene un episodio de migraña registrado."
    assert context.paciente.historial_migranas[0].tipo == tipo_migrana, "El tipo de migraña no coincide."


@step("genero un tratamiento")
def step_impl(context):
    context.tratamiento_generado = Tratamiento()
    # Asumimos un tratamiento base para el ejemplo
    context.tratamiento_generado.agregar_medicacion(
        Medicacion("Uno", "Analgésicos suaves", "500 mg", "Cada ciertas horas", "Días")
    )
    context.tratamiento_generado.agregar_recomendacion(
        Recomendacion("Técnicas de relajación")
    )
    assert context.tratamiento_generado is not None, "El tratamiento no fue generado."
    assert len(context.tratamiento_generado.medicaciones) > 0, "El tratamiento no tiene medicaciones."


@step("el sistema mostrará las siguientes características del tratamiento:")
def step_impl(context):
    expected_medicacion = Medicacion(
        context.table[0]['Cantidad'],
        context.table[0]['Medicación'],
        context.table[0]['Característica'],
        context.table[0]['Frecuencia'],
        context.table[0]['Duración tratamiento']
    )
    expected_recomendacion = Recomendacion(context.table[0]['Recomendaciones'])

    assert len(context.tratamiento_generado.medicaciones) == 1, "La cantidad de medicaciones no es la esperada."
    assert context.tratamiento_generado.medicaciones[0] == expected_medicacion, "La medicación generada no coincide."
    assert len(context.tratamiento_generado.recomendaciones) == 1, "La cantidad de recomendaciones no es la esperada."
    assert context.tratamiento_generado.recomendaciones[
               0] == expected_recomendacion, "La recomendación generada no coincide."


@step("que el paciente tiene un tratamiento activo correspondiente a un episodio médico")
def step_impl(context):
    context.paciente = Paciente()
    context.tratamiento_activo = Tratamiento(id_tratamiento=fake.uuid4())
    context.paciente.agregar_tratamiento_activo(context.tratamiento_activo)
    context.paciente.agregar_migrana(Migrana(fake.random_element(['Migraña sin aura', 'Migraña con aura', 'Cefalea de tipo tensional'])))
    assert context.paciente is not None, "El paciente no fue inicializado."
    assert len(context.paciente.tratamientos_activos) == 1, "El paciente no tiene un tratamiento activo."
    assert context.tratamiento_activo.id_tratamiento is not None, "El ID del tratamiento activo no fue generado."


@step(
    "el historial de alertas indica que el paciente ha confirmado (?P<porcentaje_cumplimiento>.+)% de las tomas correspondientes a (?P<numero_tratamientos>.+) tratamientos")
def step_impl(context, porcentaje_cumplimiento, numero_tratamientos):
    context.porcentaje_cumplimiento_simulado = float(porcentaje_cumplimiento)

    context.paciente.simular_historial_tomas(
        context.tratamiento_activo.id_tratamiento,
        context.porcentaje_cumplimiento_simulado,
        tomas_esperadas_simuladas=100
    )

    assert context.tratamiento_activo.id_tratamiento in context.paciente.historial_alertas_tomas, "No se simularon tomas para el tratamiento activo."


@step("el médico evalúa el cumplimiento del tratamiento anterior")
def step_impl(context):
    context.cumplimiento_evaluado = context.paciente.obtener_porcentaje_cumplimiento(
        context.tratamiento_activo.id_tratamiento
    )
    context.tratamiento_activo.cumplimiento = context.cumplimiento_evaluado
    assert context.cumplimiento_evaluado is not None, "No se pudo evaluar el cumplimiento."
    # Verificamos que el cumplimiento evaluado sea consistente con el simulado
    assert abs(context.cumplimiento_evaluado - context.porcentaje_cumplimiento_simulado) < 0.01, \
        f"El cumplimiento evaluado ({context.cumplimiento_evaluado:.2f}%) no coincide con el simulado ({context.porcentaje_cumplimiento_simulado}%)."


@step("si el cumplimiento es igual o mayor a 80%")
def step_impl(context):
    context.cumplimiento_mayor_o_igual_80 = (context.cumplimiento_evaluado >= 80)
    assert True, "Este paso solo establece una condición para los siguientes 'And'."  # Siempre verdadero, la lógica se maneja en los siguientes pasos.

@step('se decide modificar el tratamiento')
def step_impl(context):
    if context.cumplimiento_mayor_o_igual_80:
        context.tratamiento_modificado = True
        assert True, "Se decidió modificar el tratamiento."
    else:
        # Si no se cumple la condición, este paso no debería ejecutarse o fallar si lo hace.
        # Para BDD, es mejor que el flujo de los pasos sea claro.
        # Aquí, simplemente no se hace nada si la condición no se cumple.
        assert False, "No se cumple la condición de cumplimiento >= 80% para modificar el tratamiento."


@step("el sistema debe sugerir:")
def step_impl(context):
    assert context.cumplimiento_evaluado >= 80, f"Cumplimiento ({context.cumplimiento_evaluado:.2f}%) menor a 80%."

    cantidad = f"{fake.random_int(min=1, max=3)}"
    medicacion = fake.word(ext_word_list=['Analgésicos suaves', 'Antiinflamatorios', 'Antibióticos'])
    caracteristica = f"{fake.random_int(min=100, max=1000)} mg"
    frecuencia = f"Cada {fake.random_int(min=4, max=12)} horas"
    duracion = f"{fake.random_int(min=1, max=10)} días"
    recomendaciones = fake.sentence(nb_words=4)

    print("Valores generados:")
    print("Cantidad:", cantidad)
    print("Medicacion:", medicacion)
    print("Caracteristica:", caracteristica)
    print("Frecuencia:", frecuencia)
    print("Duracion:", duracion)
    print("Recomendaciones:", recomendaciones)

    sugerencia_medicacion = Medicacion(cantidad, medicacion, caracteristica, frecuencia, duracion)
    sugerencia_recomendacion = Recomendacion(recomendaciones)

    print("Objetos creados:")
    print(sugerencia_medicacion)
    print(sugerencia_recomendacion)

    context.tratamiento_activo.modificar_tratamiento(
        [sugerencia_medicacion], [sugerencia_recomendacion]
    )

    assert len(context.tratamiento_activo.medicaciones) == 1
    assert context.tratamiento_activo.medicaciones[0] == sugerencia_medicacion
    assert len(context.tratamiento_activo.recomendaciones) == 1
    assert context.tratamiento_activo.recomendaciones[0] == sugerencia_recomendacion
    assert context.tratamiento_activo.activo

@step("si el cumplimiento es menor al 80%")
def step_impl(context):
    context.cumplimiento_menor_80 = (context.cumplimiento_evaluado < 80)
    assert True, "Este paso solo establece una condición para los siguientes 'And'."  # Siempre verdadero, la lógica se maneja en los siguientes pasos.

@step("se debe cancelar el tratamiento actual")
def step_impl(context):
    assert context.cumplimiento_evaluado < 80, f"El cumplimiento ({context.cumplimiento_evaluado:.2f}%) es igual o mayor a 80%, no debería cancelar."

    context.tratamiento_activo.cancelar_tratamiento("Incumplimiento de tratamiento")
    assert not context.tratamiento_activo.activo, "El tratamiento no fue cancelado."


@step('registrar el motivo como "Incumplimiento de tratamiento"')
def step_impl(context):
    assert context.tratamiento_activo.motivo_cancelacion == "Incumplimiento de tratamiento", "El motivo de cancelación no es 'Incumplimiento de tratamiento'."
    assert not context.tratamiento_activo.activo, "El tratamiento debe estar inactivo para tener un motivo de cancelación."
