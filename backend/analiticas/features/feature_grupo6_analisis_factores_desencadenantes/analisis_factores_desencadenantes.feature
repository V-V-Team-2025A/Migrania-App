# Created by Joffre at 8/7/2025
# language: es
Característica: Análisis de factores desencadenantes
  Como paciente que sufre cefalea
  Quiero observar semanalmente los factores que se repiten en mis episodios
  Para prevenir futuras crisis y saber cuándo consultar con un médico


  Escenario: Factores desencadenantes
    Dado que el paciente tiene un historial de al menos 7 días de episodios de cefalea registrados:
      | categoria_esperada | duracion_cefalea_horas | severidad  | localizacion | caracter_dolor | empeora_actividad | nauseas_vomitos | presencia_aura | sintomas_aura | duracion_aura_minutos | día         | fotofobia | fonofobia |
      | "Migraña sin aura" | 5                      | "Severa"   | "Unilateral" | "Pulsátil"     | "Sí"              | "Sí"            | "No"           | "Ninguno"     | 0                     | "Lunes"     | "No"      | "Sí"      |
      | "Migraña sin aura" | 7                      | "Moderada" | "Unilateral" | "Pulsátil"     | "Sí"              | "No"            | "No"           | "Ninguno"     | 0                     | "Miércoles" | "Sí"      | "Sí"      |
      | "Migraña con aura" | 5                      | "Severa"   | "Unilateral" | "Pulsátil"     | "Sí"              | "Sí"            | "Sí"           | "Visuales"    | 25                    | "Jueves"    | "No"      | "Sí"      |
    
    Cuando se identifican factores desencadenantes recurrentes relacionados síntomas clínicos o situaciones que requieren una evaluación médica,
    Entonces se genera una alerta con el mensaje "Patrón de factores médicos o clínicos identificados"
    Y se recomienda contactar a un profesional de salud para una evaluación adicional.

  Escenario: Factores no desencadenantes
    Dado que el paciente tiene un historial de al menos 7 días de episodios de cefalea registrados:
      | categoria_esperada          | duracion_cefalea_horas | severidad  | localizacion | caracter_dolor | empeora_actividad | nauseas_vomitos | presencia_aura | sintomas_aura | duracion_aura_minutos | día         | fotofobia | fonofobia |     
      | "Migraña sin aura"          | 4                      | "Leve"     | "Bilateral"  | "Pulsátil"     | "Sí"              | "No"            | "No"           | "Ninguno"     | 0                     | "Lunes"     | "Sí"      | "No"      |
      | "Migraña sin aura"          | 3                      | "Moderada" | "Bilateral"  | "Opresivo"     | "Sí"              | "Sí"            | "No"           | "Ninguno"     | 0                     | "Martes"    | "No"      | "No"      |
      | "Migraña con aura"          | 6                      | "Leve"     | "Unilateral" | "Pulsátil"     | "No"              | "No"            | "Sí"           | "Visuales"    | 15                    | "Miércoles" | "Sí"      | "No"      | 
      | "Cefalea de tipo tensional" | 2                      | "Leve"     | "Bilateral"  | "Opresivo"     | "No"              | "No"            | "No"           | "Ninguno"     | 0                     | "Jueves"    | "No"      | "No"      |
      | "Migraña sin aura"          | 5                      | "Moderada" | "Bilateral"  | "Pulsátil"     | "Sí"              | "Sí"            | "No"           | "Ninguno"     | 0                     | "Viernes"   | "Sí"      | "Sí"      |

    Cuando se evalúan los factores asociados en los episodios recientes y no se detecta ningún patrón coherente entre ellos,
    Entonces se genera una alerta con el mensaje "No se identificaron factores desencadenantes significativos en los episodios recientes"
    Y se recomienda continuar el monitoreo para identificar factores adicionales.

  Escenario: Detección de patrones de recurrencia en días de la semana
    Dado que el paciente tiene un historial de episodios de cefalea registrados durante las últimas semanas:
      | dia         | categoria_esperada          | severidad  |
      | "Lunes"     | "Migraña sin aura"          | "Moderada" |
      | "Miércoles" | "Migraña con aura"          | "Leve"     |
      | "Viernes"   | "Cefalea de tipo tensional" | "Leve"     |
      | "Viernes"   | "Migraña sin aura"          | "Severa"   |
      | "Jueves"    | "Migraña sin aura"          | "Severa"   |
      | "Lunes"     | "Migraña sin aura"          | "Moderada" |
      | "Martes"    | "Cefalea de tipo tensional" | "Severa"   |
      | "Martes"    | "Migraña sin aura"          | "Severa"   |
      | "Martes"    | "Migraña con aura"          | "Leve"     |
      | "Martes"    | "Migraña sin aura"          | "Severa"   |
      | "Martes"    | "Migraña sin aura"          | "Moderada" |

    Cuando se identifica un patrón donde los episodios ocurren de forma repetida en los mismos días de la semana
    Entonces se genera una alerta con el mensaje "Patrón de recurrencia semanal detectado en los siguientes días: <dias_recurrentes>"
    Y se sugiere analizar las rutinas o posibles factores asociados a esos días para identificar la causa.
