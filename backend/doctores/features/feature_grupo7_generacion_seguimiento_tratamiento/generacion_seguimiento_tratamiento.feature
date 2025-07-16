# language: es
# Created by CamilaL at 7/7/2025

Característica: Generación y seguimiento de tratamiento médico

  Como médico
  Quiero saber la información médica del paciente
  Para crear un tratamiento médico que mejore la calidad de vida del paciente
  Y sea personalizado según la categorizacion (migraña sin aura, migraña con aura, cefalea de tipo tensional)

  Antecedentes:
    Dado que el paciente tiene al menos un historial de migrañas

  Esquema del escenario: Generar tratamiento según tipo de migraña
    Dado que el paciente presenta su primer episodio con la categorización <tipo_migraña>
    Cuando genero un tratamiento
    Entonces el sistema debe sugerir:
      | Tipo tratamiento     | Preventivo básico       |
      | Medicación           | Analgésicos suaves      |
      | Frecuencia           | Horas                   |
      | Duración tratamiento | Días                    |
      | Recomendaciones      | Técnicas de relajación  |

    Ejemplos:
      | tipo_migraña              |
      | Migraña sin aura         |
      | Migraña con aura         |
      | Cefalea de tipo tensional|

  Esquema del escenario: Seguimiento de tratamiento activo según cumplimiento
    Dado que el paciente tiene un tratamiento activo de un episodio
    Y el historial de alertas indica que el paciente ha confirmado <porcentaje_confirmado>% de las tomas
    Cuando el médico evalúa el cumplimiento del tratamiento anterior

    Entonces si el cumplimiento es igual o mayor a 80%
    Y se decide modificar el tratamiento
    Entonces el sistema debe sugerir:
      | Tipo tratamiento    | Intensivo y preventivo   |
      | Medicación          | Triptanes + preventivos  |
      | Frecuencia          | Diaria (preventivo)      |
      | Recomendaciones     | Derivación a especialista|

    Pero si el cumplimiento es menor a 80%
    Entonces se debe cancelar el tratamiento actual
    Y registrar el motivo como "incumplimiento de tratamiento"

    Ejemplos:
      | porcentaje_confirmado |
      | 85                    |
      | 60                    |