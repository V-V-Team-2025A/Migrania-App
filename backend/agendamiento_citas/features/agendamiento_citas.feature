Característica: : Agendamiento de citas medicas
  Como paciente,
  quiero agendar una cita médica con un doctor disponible,
  para recibir atención médica en el momento más conveniente.

Esquema del escenario: Solicitar una cita de primera vez
  Dado que <nombre_paciente> no ha realizado ningún agendamiento previamente
  Y hay disponibilidad con el doctor <doctor> el <fecha_cita> a las <hora_cita>
  Cuando el paciente agenda su cita por primera vez
  Entonces el doctor <doctor> se convierte en su médico de preferencia
  Y el paciente recibe un recordatorio para el <fecha_recordatorio> a las <hora_recordatorio>
    Ejemplos:
      | nombre_paciente | doctor     | fecha_cita | hora_cita | fecha_recordatorio | hora_recordatorio |
      | Laura Gómez     | Dr. Salas  | 2025-07-18 | 09:00     | 2025-07-17         | 09:00             |


Esquema del escenario: Solicitar una cita regular
    Dado que <nombre_paciente> tiene asignado al doctor <doctor>
    Y hay disponibilidad el <fecha_cita> a las <hora_cita>
    Cuando el paciente agenda una atención regular
    Entonces el paciente recibe un recordatorio para el <fecha_recordatorio> a las <hora_recordatorio>
      Ejemplos:
        | nombre_paciente | doctor      | fecha_cita | hora_cita | fecha_recordatorio | hora_recordatorio |
        | Juan Pérez      |Dr. García   | 2025-07-15 | 10:00     | 2025-07-14         | 10:00             |
        | Ana Torres      | Dra. Rivas  | 2025-07-16 | 09:00     | 2025-07-15         | 09:00             |


Escenario: Solicitar atención médica urgente
    Dado que el paciente presenta un historial médico de alta urgencia
    Cuando el paciente agenda una atención medica urgente
    Entonces se asigna un doctor en menos de 2 horas
    Y se reorganiza la cita médicas regulares en caso de ser necesario


Esquema del escenario: Cambiar una cita por parte del paciente
    Dado que <nombre_paciente> tiene una cita agendada con el doctor <doctor> el <fecha_original> a las <hora_original>
    Y solicita una reprogramación con al menos 24 horas de anticipación
    Cuando se analiza la disponibilidad del doctor
    Entonces se sugiere automáticamente un horario alternativo disponible
    Y se reorganiza la cita y notifica a ambas partes
      Ejemplos:
        | nombre_paciente | doctor | fecha_original | hora_original |
        | Juan Pérez      | Dr. García | 2025-07-15     | 10:00         |

Escenario: Cambiar una cita por parte del doctor
    Dado que el doctor notifica una ausencia médica
    Y existen citas agendadas durante ese periodo
    Cuando se detecta un conflicto entre las citas y el periodo de ausencia
    Entonces  se reasigna automáticamente la cita del paciente al siguiente doctor disponible
    Y se notifica al paciente con los nuevos detalles