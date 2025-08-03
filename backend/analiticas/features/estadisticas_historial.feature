#language: es

Característica: Estadística e historial

  Como médico,
  Quiero acceder al historial clínico y estadísticas detalladas relacionadas con episodios de migraña de mis pacientes o posibles pacientes,
  Para personalizar el tratamiento y apoyar el diagnóstico de manera efectiva.

#POSITIVO
Escenario: Generar historial clínico consolidado a partir de datos registrados
  Dado que un paciente ha registrado al menos una biracota digital de cefalea
  Y ha realizado al menos una autoevaluación MIDAS con puntaje válido
  Cuando el médico accede al historial clínico consolidado del paciente
  Entonces el sistema genera un historial que incluye:
    | Componente                               | Detalle esperado                                  |
    | Episodios de cefalea                     | Listado con fecha, severidad y categoría clínica  |
    | Autoevaluaciones MIDAS                   | Puntajes registrados y fechas de aplicación       |
    | Tratamientos/En caso de tener            | Medicación prescrita, dosis y fecha de inicio     |

#NEGATIVO
Escenario: Intentar generar historial clínico consolidado sin registros suficientes
  Dado que un paciente no ha registrado ningún episodio de cefalea
  Y no ha realizado ninguna autoevaluación MIDAS
  Cuando el médico accede a la opción para generar el historial clínico consolidado del paciente
  Entonces el sistema muestra un mensaje indicando que no hay información clínica disponible para consolidar

#POSITIVO
Escenario: Generar historial clínico consolidado filtrado por rango de fechas
  Dado que un paciente ha registrado al menos una biracota digital de cefalea
  Y ha realizado al menos una autoevaluación MIDAS con puntaje válido
  Cuando el médico filtra el historial clínico consolidado del paciente usando un rango de fechas entre "<fecha_inicio>" y "<fecha_fin>"
  Entonces el sistema incluye únicamente los registros cuyo campo de fecha se encuentra dentro del intervalo definido
    | Componente              | Condición de inclusión en el historial            |
    | Episodios de cefalea    | Fecha del episodio está dentro del rango         |
    | Autoevaluaciones MIDAS  | Fecha de realización está dentro del rango       |
    | Tratamientos            | Fecha de inicio del tratamiento está en el rango |

#NEGATIVO
Escenario: Intentar generar historial clínico consolidado cuando no existen registros dentro del rango de fechas
  Dado que un paciente ha registrado al menos una bitácora digital de cefalea
  Y ha realizado al menos una autoevaluación MIDAS con puntaje válido
  Cuando el médico filtra el historial clínico consolidado del paciente usando un rango de fechas entre "<fecha_inicio>" y "<fecha_fin>"
  Pero no existen registros dentro de ese intervalo de tiempo
  Entonces el sistema muestra un mensaje indicando que no se encontraron registros clínicos en el intervalo seleccionado

Escenario: Generar estadísticas clínicas a partir de los episodios registrados en la bitácora de cefalea
  Dado que un paciente ha registrado al menos <minimo_episodios> episodios en su bitácora digital de cefalea con sus respectivos síntomas, severidad y fechas
  Cuando el médico genera del resumen estadístico clínico de  los episodios de cefalea del paciente
  Entonces el sistema presenta un conjunto de indicadores clínicos calculados a partir de los registros, incluyendo:
    | Estadística                              | Cálculo esperado                                                        |
    | Frecuencia total de episodios            | Número total de episodios registrados                                  |
    | Promedio de episodios por mes            | Frecuencia mensual estimada según fechas registradas                   |
    | Severidad promedio del dolor             | Media de los niveles: Leve = 1, Moderada = 2, Severa = 3               |
    | Duración promedio de los episodios       | Promedio de la duración en horas                                        |
    | Porcentaje por tipo de cefalea           | Clasificación automática: migraña con aura, sin aura, tensional        |
    | Frecuencia de síntomas acompañantes      | Porcentaje de episodios con náuseas, fotofobia, fonofobia, etc.        |
    | Asociación con menstruación (si aplica)  | Número y porcentaje de episodios ocurridos durante el ciclo menstrual  |
Ejemplos:
  | minimo_episodios |
  | 3                |

Escenario: Generar estadísticas clínicas a partir de autoevaluaciones MIDAS registradas
  Dado que un paciente ha realizado al menos <minimo_autoevaluaciones> autoevaluaciones MIDAS con sus respectivos puntajes y fechas
  Cuando el médico genera del resumen estadístico clínico de  las autoevaluaciones MIDAS del paciente
  Entonces el sistema presenta un conjunto de indicadores clínicos derivados de las autoevaluaciones, incluyendo:
    | Estadística                              | Cálculo esperado                                                  |
    | Puntaje MIDAS más reciente               | Valor y fecha del último test                                     |
    | Promedio de puntajes MIDAS               | Media de todos los puntajes registrados                          |
    | Clasificación promedio de discapacidad   | Según rango: leve, moderada, severa                              |
    | Tendencia de evolución del puntaje       | Mejora, estabilidad o deterioro a lo largo del tiempo            |
Ejemplos:
  | minimo_autoevaluaciones |
  | 2                       |

Escenario: Generar estadísticas clínicas a partir de tratamientos registrados

  Dado que un paciente ha recibido al menos <minimo_tratamientos> tratamientos con sus respectivas fechas, tipos de medicación y seguimiento clínico
  Cuando el médico genera del resumen estadístico del historial de tratamientos del paciente
  Entonces el sistema presenta indicadores clínicos relevantes, incluyendo:
    | Estadística                            | Cálculo esperado                                                     |
    | Total de tratamientos aplicados        | Número de tratamientos distintos registrados                        |
    | Promedio de duración por tratamiento   | Diferencia entre fecha de inicio y fecha de modificación o cierre   |
    | Variación promedio del nivel de dolor  | Diferencia entre nivel de dolor inicial y final por tratamiento     |
    | Porcentaje de tratamientos efectivos   | Casos con reducción significativa de dolor o frecuencia              |
    | Frecuencia de ajustes                  | Número de veces que se modificó un tratamiento activo                |
Ejemplos:
  | minimo_tratamientos |
  | 2                   |