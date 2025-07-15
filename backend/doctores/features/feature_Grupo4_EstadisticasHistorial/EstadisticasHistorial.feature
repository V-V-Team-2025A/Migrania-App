#language: es

Característica: Estadística e historial

  Como médico,
  Quiero acceder al historial clínico y estadísticas detalladas relacionadas con episodios de migraña de mis pacientes o posibles pacientes,
  Para personalizar el tratamiento y apoyar el diagnóstico de manera efectiva.

#POSITIVO
Escenario: Generar historial clínico consolidado a partir de datos registrados
  Dado que un paciente ha registrado al menos un episodio de cefalea con su respectiva fecha y síntomas
  Y ha realizado al menos una autoevaluación MIDAS con puntaje válido
  Y ha sido asignado un tratamiento con medicamento, dosis y fecha de inicio
  Cuando el médico genera el historial clínico consolidado del paciente
  Entonces el sistema genera un historial que incluye:
    | Componente              | Detalle esperado                                  |
    | Episodios de cefalea    | Listado con fecha, severidad y categoría clínica  |
    | Autoevaluaciones MIDAS  | Puntajes registrados y fechas de aplicación       |
    | Tratamientos            | Medicación prescrita, dosis y fecha de inicio     |

#NEGATIVO
Escenario: Intentar generar historial clínico consolidado sin registros suficientes
  Dado que un paciente no ha registrado ningún episodio de cefalea
  Y no ha realizado ninguna autoevaluación MIDAS
  Cuando el médico accede a la opción para generar el historial clínico consolidado del paciente
  Entonces el sistema muestra un mensaje indicando que no hay información clínica disponible para consolidar

