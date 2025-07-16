# Created by Joffre at 8/7/2025
# language: es
Característica: Análisis de factores desencadenantes
  Como paciente que sufre cefalea
  Quiero observar semanalmente los factores que se repiten en mis episodios
  Para prevenir futuras crisis y saber cuándo consultar con un médico


  Escenario: Factores desencadenantes
    Dado que el paciente tiene un historial de al menos 7 días de episodios de cefalea registrados,
    Cuando se identifican factores desencadenantes recurrentes relacionados con medicamentos, síntomas clínicos o situaciones que requieren una evaluación médica,
    Entonces se genera una alerta con el mensaje "Patrón de factores médicos o clínicos identificados"
    Y se recomienda contactar a un profesional de salud para una evaluación adicional.

    Ejemplo:
      | categoria_esperada  | duracion_cefalea_horas   | severidad  | localizacion | caracter_dolor  | empeora_actividad  | nauseas_vomitos  | fotofobia | fonofobia | presencia_aura  | sintomas_aura          | duracion_aura_minutos   | día         |
      | "Migraña sin aura"  | 5                        | "Severa"   | "Unilateral" | "Pulsátil"      | "Sí"               | "Sí"             | "No"      | "Sí"      | "No"            | "Ninguno"              | 0                       | "Lunes"     |
      | "Migraña sin aura"  | 7                        | "Moderada" | "Unilateral" | "Pulsátil"      | "Sí"               | "No"             | "Sí"      | "Sí"      | "No"            | "Ninguno"              | 0                       | "Miércoles" |
      | "Migraña con aura"  | 5                        | "Severa"   | "Unilateral" | "Pulsátil"      | "Sí"               | "Sí"             | "No"      | "Sí"      | "Sí"            | "Visuales"             | 25                      | "Jueves"    |


  Escenario: Factores no desencadenantes
    Dado que el paciente tiene un historial de al menos 7 días de episodios de cefalea registrados,
    Cuando se evalúan los factores asociados en los episodios recientes y no se detecta ningún patrón coherente entre ellos,
    Entonces se genera una alerta con el mensaje "No se identificaron factores desencadenantes significativos en los episodios recientes"
    Y se recomienda continuar el monitoreo para identificar factores adicionales.

    # todo: cambiar datos para uqe no exista patrón
    Ejemplo:
      | categoria_esperada          | duracion_cefalea_horas   | severidad  | localizacion | caracter_dolor  | empeora_actividad  | nauseas_vomitos  | fotofobia | fonofobia | presencia_aura  | sintomas_aura  | duracion_aura_minutos   | día         |      
      | "Migraña sin aura"          | 4                        | "Leve"     | "Bilateral"  | "Pulsátil"      | "Sí"               | "No"             | "Sí"      | "No"      | "No"            | "Ninguno"      | 0                       | "Lunes"     |
      | "Migraña sin aura"          | 3                        | "Moderada" | "Bilateral"  | "Opresivo"      | "Sí"               | "Sí"             | "No"      | "No"      | "No"            | "Ninguno"      | 0                       | "Martes"    |
      | "Migraña con aura"          | 6                        | "Leve"     | "Unilateral" | "Pulsátil"      | "No"               | "No"             | "Sí"      | "No"      | "Sí"            | "Visuales"     | 15                      | "Miércoles" |
      | "Cefalea de tipo tensional" | 2                        | "Leve"     | "Bilateral"  | "Opresivo"      | "No"               | "No"             | "No"      | "No"      | "No"            | "Ninguno"      | 0                       | "Jueves"    |
      | "Migraña sin aura"          | 5                        | "Moderada" | "Bilateral"  | "Pulsátil"      | "Sí"               | "Sí"             | "Sí"      | "Sí"      | "No"            | "Ninguno"      | 0                       | "Viernes"   |


  # todo: Recurrencia en días por varias semanas 
  Escenario: Detección de patrones de recurrencia en días de la semana
    Dado que el paciente tiene un historial de episodios de cefalea registrados durante las últimas semanas
    Cuando se identifica un patrón donde los episodios ocurren de forma repetida en los mismos días de la semana
    Entonces se genera una alerta con el mensaje "Patrón de recurrencia semanal detectado en los siguientes días: <dias_recurrentes>"
    Y se sugiere analizar las rutinas o posibles factores asociados a esos días para identificar la causa.

    Ejemplo:
      | categoria_esperada          | duracion_cefalea_horas   | severidad  | localizacion | caracter_dolor  | empeora_actividad  | nauseas_vomitos  | fotofobia | fonofobia | presencia_aura  | sintomas_aura          | duracion_aura_minutos   | día         |
      | "Migraña sin aura"          | 5                        | "Moderada" | "Unilateral" | "Pulsátil"      | "Sí"               | "Sí"             | "Sí"      | "No"      | "No"            | "Ninguno"              | 0                       | "Lunes"     |
      | "Migraña sin aura"          | 6                        | "Severa"   | "Bilateral"  | "Pulsátil"      | "Sí"               | "Sí"             | "No"      | "No"      | "No"            | "Ninguno"              | 0                       | "Martes"    |
      | "Migraña con aura"          | 4                        | "Leve"     | "Unilateral" | "Opresivo"      | "Sí"               | "No"             | "Sí"      | "Sí"      | "Sí"            | "Visuales"             | 20                      | "Miércoles" |
      | "Migraña sin aura"          | 3                        | "Leve"     | "Bilateral"  | "Pulsátil"      | "No"               | "Sí"             | "No"      | "No"      | "No"            | "Ninguno"              | 0                       | "Martes"    |
      | "Cefalea de tipo tensional" | 2                        | "Leve"     | "Bilateral"  | "Opresivo"      | "No"               | "No"             | "No"      | "No"      | "No"            | "Ninguno"              | 0                       | "Viernes"   |
      | "Migraña sin aura"          | 4                        | "Moderada" | "Unilateral" | "Pulsátil"      | "Sí"               | "No"             | "No"      | "No"      | "No"            | "Ninguno"              | 0                       | "Martes"    |
      | "Migraña sin aura"          | 6                        | "Severa"   | "Unilateral" | "Pulsátil"      | "Sí"               | "Sí"             | "Sí"      | "Sí"      | "No"            | "Ninguno"              | 0                       | "Viernes"   |
      | "Migraña con aura"          | 5                        | "Leve"     | "Unilateral" | "Pulsátil"      | "No"               | "No"             | "Sí"      | "No"      | "Sí"            | "Visuales, Sensitivos" | 15                      | "Martes"    |
      | "Migraña sin aura"          | 7                        | "Severa"   | "Bilateral"  | "Pulsátil"      | "Sí"               | "Sí"             | "No"      | "Sí"      | "No"            | "Ninguno"              | 0                       | "Jueves"    |
      | "Migraña sin aura"          | 5                        | "Moderada" | "Unilateral" | "Pulsátil"      | "Sí"               | "No"             | "Sí"      | "No"      | "No"            | "Ninguno"              | 0                       | "Lunes"     |
      | "Cefalea de tipo tensional" | 2                        | "Leve"     | "Bilateral"  | "Opresivo"      | "No"               | "No"             | "No"      | "No"      | "No"            | "Ninguno"              | 0                       | "Martes"    |
