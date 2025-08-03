# -*- coding: utf-8 -*-
"""
Steps para el testing BDD de estadísticas del historial.
Solo implementa el primer escenario: "Análisis del promedio semanal de episodios de migraña"
Usando el archivo estadistica_historial_services.py
"""

from behave import *
from datetime import datetime, timedelta
from django.utils import timezone

use_step_matcher("re")


# Background steps
@given(r"que el paciente tiene al menos tres episodios registrados en su bitácora digital")
def step_background_episodios(context):
    """Configura el contexto básico con repositorios y un paciente"""
    # Importar desde tu archivo consolidado
    from usuarios.repositories import FakeUserRepository
    from analiticas.estadistica_historial_services import FakeAnalyticRepository, AnalyticService
    
    # Configurar repositorios fake
    context.user_repository = FakeUserRepository()
    context.analytic_repository = FakeAnalyticRepository()
    context.analytic_service = AnalyticService(context.analytic_repository)
    
    # Crear usuario de prueba (paciente)
    user_data = {
        'username': "paciente_test",
        'email': "paciente@test.com",
        'password': "password123",
        'first_name': "Juan",
        'last_name': "Pérez",
        'cedula': "0503099533",
        'telefono': '1234567890',
        'fecha_nacimiento': '1990-01-01'
    }
    
    profile_data = {
        'contacto_emergencia_nombre': 'Contacto Test',
        'contacto_emergencia_telefono': '0987654321',
        'contacto_emergencia_relacion': 'Familiar'
    }
    
    context.paciente = context.user_repository.create_paciente(user_data, profile_data)


@given(r"cuenta al menos tres evaluaciones MIDAS completadas")
def step_background_midas(context):
    """Configura evaluaciones MIDAS básicas"""
    # Por ahora solo creamos el contexto, las evaluaciones específicas se crean en cada escenario
    pass


# Steps específicos para el primer escenario
@given(r"que el paciente tiene (\d+) episodios registrados en su bitácora digital")
def step_paciente_episodios_especificos(context, total_episodios):
    """Configura episodios específicos para el escenario"""
    context.total_episodios = int(total_episodios)


@given(r"el primer episodio fue registrado en la fecha (\d{4}-\d{2}-\d{2})")
def step_primer_episodio_fecha(context, fecha_inicio_str):
    """Establece la fecha del primer episodio"""
    context.fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()


@given(r"el último episodio fue registrado en la fecha (\d{4}-\d{2}-\d{2})")
def step_ultimo_episodio_fecha(context, fecha_fin_str):
    """Establece la fecha del último episodio y crea todos los episodios"""
    context.fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
    
    # Ahora que tenemos todas las fechas, crear los episodios distribuidos
    dias_totales = (context.fecha_fin - context.fecha_inicio).days
    intervalo_dias = dias_totales / (context.total_episodios - 1) if context.total_episodios > 1 else 0
    
    for i in range(context.total_episodios):
        fecha_episodio = context.fecha_inicio + timedelta(days=int(i * intervalo_dias))
        
        # Convertir la fecha a datetime para el modelo
        fecha_inicio_datetime = timezone.make_aware(
            datetime.combine(fecha_episodio, datetime.min.time())
        )
        
        datos_episodio = {
            'fecha_inicio': fecha_inicio_datetime,
            'duracion_horas': 4.0  # 4 horas de duración
        }
        context.analytic_repository.crear_episodio_migrana(context.paciente, datos_episodio)


@when(r"solicito el análisis del promedio semanal")
def step_solicitar_analisis_promedio(context):
    """Solicita el análisis del promedio semanal"""
    # Realizar el cálculo del promedio semanal usando fechas como strings
    fecha_inicio_str = context.fecha_inicio.strftime('%Y-%m-%d')
    fecha_fin_str = context.fecha_fin.strftime('%Y-%m-%d')
    
    context.promedio_semanal_calculado = context.analytic_service.calcular_promedio_semanal_episodios(
        context.paciente,
        fecha_inicio=fecha_inicio_str,
        fecha_fin=fecha_fin_str
    )


@then(r"el sistema mostrará que el promedio semanal de episodios es ([\d.]+) veces")
def step_verificar_promedio_semanal(context, promedio_esperado):
    """Verifica que el promedio semanal calculado sea correcto"""
    promedio_esperado = float(promedio_esperado)
    promedio_calculado = context.promedio_semanal_calculado
    
    # Tolerancia de 0.1 para cálculos de punto flotante
    assert abs(promedio_calculado - promedio_esperado) <= 0.1, \
        f"Promedio semanal esperado: {promedio_esperado}, calculado: {promedio_calculado}"