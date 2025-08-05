# Created by Escobar Alex, Haro Rodrigo, Jacome Emilio, Mendosa Miguel at 13/7/2025
# language: es

Característica: Aseguramiento del tratamiento para la migraña
  Como paciente con tratamiento para la migraña,
  Quiero recordar las actividades definidas,
  Para cumplirlas y minimizar interrupciones en mi vida diaria.

  Esquema del escenario: Recordatorio de toma de medicamentos pendientes
    Dado que el paciente tiene una medicina prescrita para la migraña
    Y una frecuencia de dosificación cada <frecuencia> horas
    Y una duración de <dias> días
    Cuando la hora actual sea <minutos_antes> minutos antes de la hora de la toma
    Entonces se enviará un recordatorio al paciente indicando que debe tomar su medicación pronto
    Y el estado de la notificación será "activa"

    Ejemplos:
      | frecuencia | dias | minutos_antes |
      | 8          | 2    | 30            |

  Escenario: Confirmación de toma de medicamentos
    Dado que el paciente ha recibido una alerta para tomar su medicación
    Y la hora actual es la hora programada para la toma
    Cuando el paciente confirma que ha tomado la medicación
    Entonces se actualizará el estado de la alarma a "tomado"

  Escenario: Confirmación de olvido de toma de medicamentos
    Dado que el paciente ha recibido una alerta para tomar su medicación
    Y la hora actual es la hora programada para la toma
    Cuando el paciente confirma que no ha tomado la medicación
    Entonces se actualizará el estado de la alarma a "no tomado"
    Y se enviará una notificación al paciente sugiriendo que tome su medicación

  Escenario: Omisión de confirmación de toma de medicamentos
    Dado que el paciente ha recibido una alerta para tomar su medicación
    Y la hora actual es la hora programada para la toma
    Cuando transcurran 30 minutos sin que el paciente confirme la toma
    Entonces se enviará una segunda alerta
    Y se programará una tercera alerta 15 minutos después de la segunda
    Y si no se confirma ninguna de las 3 alertas, se actualizará el estado de la alerta a "sin confirmar"

  Esquema del escenario: Recordatorio de recomendación de tratamiento
    Dado que el paciente tiene una recomendación de tratamiento para la migraña
    Cuando sea las <horas> del día
    Entonces se notificará mediante un recordatorio sugiriendole seguir esta recomendación
    Y el estado de la notificación será "activa"

    Ejemplos:
      | horas |
      | 9     |
      | 18    |