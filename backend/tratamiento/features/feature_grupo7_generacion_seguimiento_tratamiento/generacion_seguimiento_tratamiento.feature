# Created by CamilaL at 7/7/2025
#language: es

Característica: Generación y seguimiento de tratamiento

  Como médico
  Quiero saber la información médica del paciente
  Para crear un tratamiento médico que mejore la calidad de vida del paciente
  Y sea personalizado según el nivel de dolor, frecuencia de ataques, tiempo de duración y desencadenante

  Antecedentes:
    Dado que el paciente tiene al menos un historial de migrañas

  Escenario: Generar tratamiento para dolor leve con baja frecuencia
    Dado que el paciente "María García" tiene:
      | Nivel de dolor      | 3/10                    |
      | Frecuencia ataques  | 1 vez por mes           |
      | Duración promedio   | 2 horas                 |
      | Desencadenante      | Cambios hormonales      |
    Cuando genero un tratamiento personalizado
    Entonces el sistema debe sugerir:
      | Tipo tratamiento    | Preventivo básico       |
      | Medicación          | Analgésicos suaves      |
      | Frecuencia          | Según necesidad         |
      | Recomendaciones     | Técnicas de relajación  |

  Escenario: Generar tratamiento para dolor severo con alta frecuencia
    Dado que el paciente "Carlos Rodríguez" tiene:
      | Nivel de dolor      | 9/10                    |
      | Frecuencia ataques  | Diario                  |
      | Duración promedio   | 6 horas                 |
      | Desencadenante      | Múltiples factores      |
    Cuando genero un tratamiento personalizado
    Entonces el sistema debe sugerir:
      | Tipo tratamiento    | Intensivo y preventivo   |
      | Medicación          | Triptanes + preventivos  |
      | Frecuencia          | Diaria (preventivo)      |
      | Recomendaciones     | Derivación a especialista|

  Escenario: Personalizar tratamiento según desencadenante específico
    Dado que el paciente "Ana López" tiene como desencadenante "Alimentos específicos"
    Y su nivel de dolor es "7/10"
    Y la frecuencia de ataques es "2 veces por semana"
    Cuando genero un tratamiento personalizado
    Entonces el sistema debe incluir:
      | Recomendación principal | Dieta de eliminación     |
      | Medicación             | Analgésicos moderados    |
      | Seguimiento            | Diario alimentario       |
      | Consulta especializada | Nutricionista            |

  Escenario: Modificar tratamiento basado en evolución del paciente
    Dado que el paciente "Pedro Martín" tiene un tratamiento activo
    Y su nivel de dolor actual es "4/10"
    Y su nivel de dolor inicial era "8/10"
    Y la frecuencia de ataques se redujo de "5 veces por semana" a "1 vez por semana"
    Cuando actualizo el tratamiento
    Entonces el sistema debe sugerir:
      | Acción              | Reducir dosis medicación |
      | Nuevo seguimiento   | Quincenal               |
      | Estado tratamiento  | Efectivo - mantener     |