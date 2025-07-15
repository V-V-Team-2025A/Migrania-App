# language: es

Característica: Evaluación MIDAS
  Como paciente
  Quiero saber mi grado de discapacidad
  Para entender mejor el impacto de migrañas en mi vida diaria

  Esquema del escenario: La evaluación está disponible luego de 3 meses
    Dado que el paciente ha realizado una última evaluación en la "<fecha>"
    Cuando pasen 3 meses desde la última evaluación
    Entonces el paciente podrá realizar una nueva evaluación

    Ejemplos:
      | fecha      | fecha_actual |
      | 2023-01-01 | 2023-04-01   |
      | 2023-12-15 | 2024-03-15   |
      | 2023-03-10 | 2023-06-10   |


  Esquema del escenario: La evaluación no está disponible
    Dado que el paciente ha realizado una última evaluación en la "<fecha>"
    Cuando no pasen 3 meses desde la última evaluación
    Entonces el paciente no podrá realizar una nueva evaluación

    Ejemplos:
      | fecha      | fecha_actual |
      | 2023-02-01 | 2023-02-02   |
      | 2023-01-15 | 2023-01-25   |
      | 2023-04-11 | 2023-04-11   |
