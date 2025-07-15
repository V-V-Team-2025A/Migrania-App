# Created by Joffre at 8/7/2025
# language: es
Característica: Análisis de factores desencadenantes de migrañas
  Como paciente que sufre migrañas
  Quiero observar regularmente los factores que se repiten en mis episodios
  Para prevenir futuras crisis y saber cuándo consultar con un médico

  Escenario: Factores desencadenantes que no requieren atención médica
    Dado que el paciente tiene un historial de al menos 7 días de episodios de migraña registrados,
    Cuando se identifican patrones en factores desencadenantes que no se relacionan con tratamientos médicos ni condiciones clínicas graves,
    Entonces se genera una alerta con el mensaje "Factores no médicos identificados como posibles desencadenantes"
    Y se sugiere tomar precauciones para evitar estos factores desencadenantes sin necesidad de intervención médica.

    Ejemplo:
      | cantidad | factores_desc  |
      | -------- | -------------- |
      | 3        | L              |
      | 4        | L,S            |

  Escenario: Factores desencadenantes que requieren atención médica
    Dado que el paciente tiene un historial de al menos 7 días de episodios de migraña registrados,
    Cuando se identifican factores desencadenantes recurrentes relacionados con medicamentos, síntomas clínicos o situaciones que requieren una evaluación médica,
    Entonces se genera una alerta con el mensaje "Patrón de factores médicos o clínicos identificados"
    Y se recomienda contactar a un profesional de salud para una evaluación adicional.

    Ejemplo:
      | cantidad | factores_desc  |
      | -------- | -------------- |
      | 3        | S,M            |
      | 4        | L,S,M          |

  Escenario: Factores no desencadenantes
    Dado que el paciente tiene un historial de al menos 7 días de episodios de migraña registrados,
    Cuando se evalúan los factores asociados en los episodios recientes y no se detecta ningún patrón coherente entre ellos,
    Entonces se genera una alerta con el mensaje "No se identificaron factores desencadenantes significativos en los episodios recientes"
    Y se recomienda continuar el monitoreo para identificar factores adicionales.

    Ejemplo:
      | factores_asociados  | cantidad_dias  |
      | ------------------- | -------------- |
      | L                   | 7              |
      | S                   | 10             |

  Escenario: Detección de patrones de recurrencia en días de la semana
    Dado que el paciente tiene un historial de episodios de migraña registrados durante las últimas semanas
    Cuando se identifica un patrón donde los episodios ocurren de forma repetida en los mismos días de la semana
    Entonces se genera una alerta con el mensaje "Patrón de recurrencia semanal detectado en los siguientes días: <dias_recurrentes>"
    Y se sugiere analizar las rutinas o posibles factores asociados a esos días para identificar la causa.

    Ejemplo:
      | semanas_analizadas | minimo_coincidencias | dias_recurrentes |
      | 4                  | 3                    | Lunes            |
      | 3                  | 3                    | Viernes          |
      | 5                  | 2                    | Martes, Jueves   |
