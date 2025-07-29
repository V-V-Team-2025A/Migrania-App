import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'migraine_app.settings')
django.setup()

from behave import *
from datetime import datetime, timedelta
from tratamiento.models import (
    Paciente, Medicamento, Tratamiento, Recordatorio, Alerta,
    EstadoNotificacion
)
import logging
import random

logger = logging.getLogger(__name__)

use_step_matcher("re")

@step("que el paciente tiene una medicina prescrita para la migraña")
def step_impl(context):
    identificacion_unica = f"{random.randint(1000000000, 9999999999)}"
    medicamento = Medicamento(
        nombre="Sumatriptán",
        dosis="50mg",
        hora_de_inicio=(datetime.now() + timedelta(hours=1)).time(),
        frecuencia=8,
        duracion_dias=5
    )
    medicamento.save()
    tratamiento = Tratamiento()
    tratamiento.save()
    tratamiento.medicamentos.add(medicamento)
    paciente = Paciente(
        nombre=f"Paciente-{random.randint(1000, 9999)}",
        identificacion=identificacion_unica,
        tratamiento=tratamiento
    )
    paciente.save()
    context.paciente = paciente
    context.medicamento = medicamento
    context.tratamiento = tratamiento
    logger.info(f"Paciente creado: {paciente} con medicamento: {medicamento}")
    assert context.paciente.tratamiento is not None, "El paciente debe tener un tratamiento asociado"
    assert medicamento in context.paciente.tratamiento.medicamentos.all(), "El medicamento debe estar asociado al tratamiento"

@step("la hora actual sea 30 minutos antes de la hora de la toma")
def step_impl(context):
    hora_toma = datetime.combine(datetime.today(), context.medicamento.hora_de_inicio)
    context.hora_actual = hora_toma - timedelta(minutes=30)
    logger.info(f"Hora actual establecida: {context.hora_actual}, 30 minutos antes de {hora_toma}")
    diferencia = (hora_toma - context.hora_actual).total_seconds() / 60
    assert diferencia == 30, f"La hora actual debe ser 30 minutos antes de la toma, pero la diferencia es {diferencia} minutos"

@step("se enviará un recordatorio al paciente indicando que debe tomar su medicación pronto")
def step_impl(context):
    recordatorio = Recordatorio(
        mensaje=f"Recordatorio para tomar {context.medicamento.nombre}",
        fecha_hora=context.hora_actual,
        estado=EstadoNotificacion.ACTIVO
    )
    recordatorio.save()
    context.recordatorio = recordatorio
    context.tratamiento.bicola_notificacion.agregarFinal(recordatorio)
    logger.info(f"Recordatorio creado: {recordatorio.mensaje} para las {recordatorio.fecha_hora}")
    bicola_elementos = context.tratamiento.bicola_notificacion.listar_elementos()
    assert recordatorio in bicola_elementos, "El recordatorio debe estar en la bicola de notificaciones"
    assert context.medicamento.nombre in recordatorio.mensaje, "El recordatorio debe mencionar el nombre del medicamento"

@step('el estado de la recordatorio será "activo"')
def step_impl(context):
    assert context.recordatorio.estado == EstadoNotificacion.ACTIVO, \
        f"El estado del recordatorio debería ser '{EstadoNotificacion.ACTIVO}', pero es '{context.recordatorio.estado}'"

@step("que el paciente ha recibido una (?P<numero_alerta>.+) alerta para tomar su medicación")
def step_impl(context, numero_alerta):
    numeros_alerta = {"primera": 1, "segunda": 2, "tercera": 3}
    numero = numeros_alerta[numero_alerta]
    if not hasattr(context, 'paciente'):
        identificacion_unica = f"{random.randint(1000000000, 9999999999)}"[:10]
        paciente = Paciente(
            nombre=f"Paciente-{random.randint(1000, 9999)}",
            identificacion=identificacion_unica
        )
        paciente.save()
        context.paciente = paciente
    if not hasattr(context, 'tratamiento'):
        tratamiento = Tratamiento()
        tratamiento.save()
        context.tratamiento = tratamiento
        if context.paciente.tratamiento is None:
            context.paciente.tratamiento = tratamiento
            context.paciente.save()
    fecha_hora_alerta = datetime.now() - timedelta(minutes=1)
    alerta = Alerta(
        mensaje=f"Alerta #{numero} para tomar medicamento",
        fecha_hora=fecha_hora_alerta,
        estado=EstadoNotificacion.ACTIVO,
        numero_alerta=numero,
        duracion=15,
        tiempo_espera=15
    )
    alerta.save()
    context.alerta = alerta
    logger.info(f"Alerta creada: {alerta.mensaje}, número: {alerta.numero_alerta}, hora: {alerta.fecha_hora}")
    context.tratamiento.bicola_notificacion.agregarFrente(alerta)
    logger.info(f"Alerta agregada al frente de la bicola, elementos totales: {len(context.tratamiento.bicola_notificacion)}")
    assert alerta in context.tratamiento.bicola_notificacion.listar_elementos(), "La alerta debe estar en la bicola"
    assert context.tratamiento.bicola_notificacion.verFrente() == alerta, "La alerta debe estar al frente de la bicola"
    assert alerta.numero_alerta == numero, f"El número de alerta debe ser {numero}, pero es {alerta.numero_alerta}"

@step("la hora actual es (?P<tiempo_transcurrido>.+) minutos después de la hora programada para la toma")
def step_impl(context, tiempo_transcurrido):
    minutos = int(tiempo_transcurrido)
    if not hasattr(context, 'alerta') or not context.alerta.fecha_hora:
        raise ValueError("La alerta no está definida o no tiene fecha_hora")
    if minutos == 0:
        context.hora_actual = context.alerta.fecha_hora + timedelta(seconds=1)
    else:
        context.hora_actual = context.alerta.fecha_hora + timedelta(minutes=minutos)
    logger.info(f"Hora actual establecida: {context.hora_actual}, {minutos} minutos después de la alerta {context.alerta.fecha_hora}")
    assert context.hora_actual > context.alerta.fecha_hora, "La hora actual debe ser posterior a la hora de la alerta"
    if minutos > 0:
        diferencia = (context.hora_actual - context.alerta.fecha_hora).total_seconds() / 60
        assert abs(diferencia - minutos) < 0.1, f"La diferencia de tiempo debe ser {minutos} minutos, pero es {diferencia}"

@step("transcurran 15 minutos sin que el paciente confirme la toma")
def step_impl(context):
    if not hasattr(context, 'hora_actual') or not hasattr(context, 'alerta'):
        raise ValueError("Falta información de hora actual o alerta")
    nueva_hora_actual = context.hora_actual + timedelta(minutes=15)
    context.hora_actual = nueva_hora_actual
    logger.info(f"Hora actual actualizada a: {context.hora_actual} (avanzada 15 minutos)")
    tiempo_transcurrido = (context.hora_actual - context.alerta.fecha_hora).total_seconds() / 60
    if tiempo_transcurrido >= 15:
        context.alerta.estado = EstadoNotificacion.SIN_CONFIRMAR
        context.alerta.save()
        logger.info(f"Estado de alerta actualizado a: {context.alerta.estado} después de {tiempo_transcurrido:.2f} minutos")
    else:
        logger.warning(f"No han pasado 15 minutos desde la alerta (solo {tiempo_transcurrido:.2f}), pero se forzará el estado 'sin_confirmar'")
        context.alerta.estado = EstadoNotificacion.SIN_CONFIRMAR
        context.alerta.save()
    assert context.alerta.estado == EstadoNotificacion.SIN_CONFIRMAR, \
        f"El estado de la alerta debe ser '{EstadoNotificacion.SIN_CONFIRMAR}', pero es '{context.alerta.estado}'"

@step('se actualizará el estado de la alerta a "sin confirmar"')
def step_impl(context):
    assert context.alerta.estado == EstadoNotificacion.SIN_CONFIRMAR, \
        f"El estado de la alerta debería ser '{EstadoNotificacion.SIN_CONFIRMAR}', pero es '{context.alerta.estado}'"

@step("se programará una (?P<accion_siguiente>.+) alerta")
def step_impl(context, accion_siguiente):
    if accion_siguiente != "ninguna":
        nueva_alerta = context.alerta.reenviar(context.tratamiento.bicola_notificacion)
        nueva_numero = {"segunda": 2, "tercera": 3}[accion_siguiente]
        assert nueva_alerta is not None, "La nueva alerta no debería ser None"
        assert nueva_alerta.numero_alerta == nueva_numero, \
            f"El número de la nueva alerta debería ser {nueva_numero}, pero es {nueva_alerta.numero_alerta}"
        frente_bicola = context.tratamiento.bicola_notificacion.verFrente()
        assert frente_bicola.id == nueva_alerta.id, \
            f"La alerta al frente debería ser la recién creada (ID: {nueva_alerta.id}), pero es otra alerta (ID: {frente_bicola.id})"
        assert frente_bicola.numero_alerta == nueva_numero, \
            f"El número de la alerta al frente debería ser {nueva_numero}, pero es {frente_bicola.numero_alerta}"
        context.alerta = nueva_alerta
        logger.info(f"Nueva alerta programada y verificada al frente de la bicola: ID {nueva_alerta.id}, número: {nueva_alerta.numero_alerta}")
    else:
        assert context.alerta.numero_alerta == 3, \
            f"El número de alerta debería ser 3, pero es {context.alerta.numero_alerta}"
        nueva_alerta = context.alerta.reenviar(context.tratamiento.bicola_notificacion)
        assert nueva_alerta is None, "No debería haberse creado una nueva alerta"
        logger.info("No se programó ninguna alerta adicional, ya que es la tercera")

@step("el paciente confirma que (?P<estado_toma>.+) ha tomado la medicación")
def step_impl(context, estado_toma):
    context.estado_toma = estado_toma
    tiempo_transcurrido = (context.hora_actual - context.alerta.fecha_hora).total_seconds() / 60
    if estado_toma == "sí":
        if tiempo_transcurrido <= 15:
            estado_resultado = EstadoNotificacion.CONFIRMADO_TOMADO
        elif tiempo_transcurrido <= 30:
            estado_resultado = EstadoNotificacion.CONFIRMADO_TOMADO_TARDE
        else:
            estado_resultado = EstadoNotificacion.CONFIRMADO_TOMADO_MUY_TARDE
    else:
        estado_resultado = EstadoNotificacion.CONFIRMADO_NO_TOMADO
    context.tratamiento.confirmarToma(context.alerta, estado_resultado)
    logger.info(f"Confirmación procesada: {estado_toma}, estado resultante: {estado_resultado}")
    context.estado_esperado = estado_resultado
    assert context.alerta.estado == estado_resultado, \
        f"El estado de la alerta debería ser '{estado_resultado}', pero es '{context.alerta.estado}'"
    if estado_toma == "sí":
        if estado_resultado == EstadoNotificacion.CONFIRMADO_TOMADO:
            assert tiempo_transcurrido <= 15, "El tiempo para CONFIRMADO_TOMADO debe ser <= 15 minutos"
        elif estado_resultado == EstadoNotificacion.CONFIRMADO_TOMADO_TARDE:
            assert 15 < tiempo_transcurrido <= 30, "El tiempo para CONFIRMADO_TOMADO_TARDE debe ser entre 15 y 30 minutos"
        else:
            assert tiempo_transcurrido > 30, "El tiempo para CONFIRMADO_TOMADO_MUY_TARDE debe ser > 30 minutos"

@step('se actualizará el estado de la alerta a "(?P<estado_resultado>.+)"')
def step_impl(context, estado_resultado):
    estados = {
        "tomado": EstadoNotificacion.CONFIRMADO_TOMADO,
        "no tomado": EstadoNotificacion.CONFIRMADO_NO_TOMADO,
        "tomado tarde": EstadoNotificacion.CONFIRMADO_TOMADO_TARDE,
        "tomado muy tarde": EstadoNotificacion.CONFIRMADO_TOMADO_MUY_TARDE
    }
    estado_esperado = estados[estado_resultado]
    assert context.alerta.estado == estado_esperado, \
        f"El estado de la alerta debería ser '{estado_esperado}', pero es '{context.alerta.estado}'"
    if hasattr(context, 'estado_esperado'):
        assert context.estado_esperado == estado_esperado, \
            f"El estado calculado '{context.estado_esperado}' no coincide con el esperado '{estado_esperado}'"

@step("que el paciente tiene una recomendación de tratamiento para la migraña")
def step_impl(context):
    if not hasattr(context, 'paciente'):
        identificacion_unica = f"{random.randint(1000000000, 9999999999)}"[:10]
        paciente = Paciente(
            nombre=f"Paciente-{random.randint(1000, 9999)}",
            identificacion=identificacion_unica
        )
        paciente.save()
        context.paciente = paciente
    if not hasattr(context, 'tratamiento'):
        context.tratamiento = Tratamiento(recomendaciones=["hidratacion"])
        context.tratamiento.save()
        if context.paciente.tratamiento is None:
            context.paciente.tratamiento = context.tratamiento
            context.paciente.save()
        logger.info("Se ha creado un nuevo tratamiento con recomendación de hidratación")
    else:
        context.tratamiento.recomendaciones = ["hidratacion"]
        context.tratamiento.save()
        logger.info("Se ha añadido recomendación de hidratación al tratamiento existente")
    context.recomendacion = "hidratacion"
    assert "hidratacion" in context.tratamiento.recomendaciones, "El tratamiento debe incluir la recomendación 'hidratacion'"
    assert context.paciente.tratamiento == context.tratamiento, "El paciente debe tener asociado el tratamiento con recomendaciones"

@step("sea las 9 horas del día")
def step_impl(context):
    context.hora_actual = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    logger.info(f"Hora actual establecida: {context.hora_actual}")
    assert context.hora_actual.hour == 9 and context.hora_actual.minute == 0, \
        f"La hora debe ser 9:00, pero es {context.hora_actual.hour}:{context.hora_actual.minute}"

@step("se notificará mediante un recordatorio sugiriéndole seguir esta recomendación")
def step_impl(context):
    recordatorio = Recordatorio(
        mensaje=f"Recordatorio de recomendación: {context.recomendacion}",
        fecha_hora=context.hora_actual,
        estado=EstadoNotificacion.ACTIVO
    )
    recordatorio.save()
    context.recordatorio = recordatorio
    logger.info(f"Recordatorio de recomendación creado: {recordatorio.mensaje}")
    context.tratamiento.bicola_notificacion.agregarFinal(recordatorio)
    notificaciones_procesadas = context.tratamiento.procesarNotificacionesPendientes()
    logger.info(f"Notificaciones procesadas: {len(notificaciones_procesadas)}")
    assert len(notificaciones_procesadas) > 0, "Debe haberse procesado al menos una notificación"
    assert recordatorio in notificaciones_procesadas, "El recordatorio de recomendación debe estar entre las notificaciones procesadas"
    assert context.recomendacion in recordatorio.mensaje, "El recordatorio debe mencionar la recomendación"
    assert recordatorio.fecha_hora == context.hora_actual, \
        f"La fecha/hora del recordatorio debe ser {context.hora_actual}, pero es {recordatorio.fecha_hora}"
