# Created by CamilaL at 7/7/2025
#language: es

Característica: Generación y seguimiento de tratamiento médico

  Como médico
  Quiero saber la información médica del paciente
  Para crear un tratamiento médico que mejore la calidad de vida del paciente
  Y sea personalizado según la categorizacion (migraña sin aura, migraña con aura,cefalea de tipo tensional)

  Antecedentes:
    Dado que el paciente tiene al menos un historial de migrañas

  Escenario: Generar tratamiento para migraña paciente masculino
    Dado que el paciente tiene su primer episodio con una de las siguientes categorizaciones:
      | Migraña sin aura            |
      | Migraña con aura            |
      | Cefalea de tipo tensional   |
    Y se verifican las siguientes características del episodio:
      | Característica           | Valor                    |
      | Duración Cefalea (horas) | <duracion_cefalea_horas> |
      | Severidad del Dolor      | <severidad>              |
      | Localización del Dolor   | <localizacion>           |
      | Carácter del Dolor       | <caracter_dolor>         |
      | Empeora con Actividad    | <empeora_actividad>      |
      | Náuseas o Vómitos        | <nauseas_vomitos>        |
      | Sensibilidad a la Luz    | <fotofobia>              |
      | Sensibilidad al Sonido   | <fonofobia>              |
      | Presencia de Aura        | <presencia_aura>         |
      | Síntomas del Aura        | <sintomas_aura>          |
      | Duración del Aura (min)  | <duracion_aura_minutos>  |
    Cuando genero un tratamiento
    Entonces el sistema debe sugerir:
      | Tipo tratamiento     | Preventivo básico       |
      | Medicación           | Analgésicos suaves      |
      | Frecuencia           | Horas                   |
      | Duracion tratamiento | Dias                    |
      | Recomendaciones      | Técnicas de relajación  |


  Escenario: Generar tratamiento para migraña paciente femenino
    Dado que el paciente tiene su primer episodio con una de las siguientes categorizaciones:
      | Migraña sin aura            |
      | Migraña con aura            |
      | Cefalea de tipo tensional   |
    Y se verifican las siguientes características del episodio:
      | Característica           | Valor                    |
      | Duración Cefalea (horas) | <duracion_cefalea_horas> |
      | Severidad del Dolor      | <severidad>              |
      | Localización del Dolor   | <localizacion>           |
      | Carácter del Dolor       | <caracter_dolor>         |
      | Empeora con Actividad    | <empeora_actividad>      |
      | Náuseas o Vómitos        | <nauseas_vomitos>        |
      | Sensibilidad a la Luz    | <fotofobia>              |
      | Sensibilidad al Sonido   | <fonofobia>              |
      | Presencia de Aura        | <presencia_aura>         |
      | Síntomas del Aura        | <sintomas_aura>          |
      | Duración del Aura (min)  | <duracion_aura_minutos>  |
      | En menstruación          | <en_menstruacion>        |
      | Anticonceptivos          | <anticonceptivos>        |
    Cuando genero un tratamiento
    Entonces el sistema debe sugerir:
      | Tipo tratamiento     | Preventivo básico       |
      | Medicación           | Analgésicos suaves      |
      | Frecuencia           | Horas                   |
      | Duracion tratamiento | Dias                    |
      | Recomendaciones      | Técnicas de relajación  |


  Escenario: Seguimiento tratamiento para paciente masculino
    Dado que el paciente tiene un tratamiento activo de un episodio
    Y se verifican el historial del o los episodios con las siguientes características:
      | Característica           | Valor                    |
      | Duración Cefalea (horas) | <duracion_cefalea_horas> |
      | Severidad del Dolor      | <severidad>              |
      | Localización del Dolor   | <localizacion>           |
      | Carácter del Dolor       | <caracter_dolor>         |
      | Empeora con Actividad    | <empeora_actividad>      |
      | Náuseas o Vómitos        | <nauseas_vomitos>        |
      | Sensibilidad a la Luz    | <fotofobia>              |
      | Sensibilidad al Sonido   | <fonofobia>              |
      | Presencia de Aura        | <presencia_aura>         |
      | Síntomas del Aura        | <sintomas_aura>          |
      | Duración del Aura (min)  | <duracion_aura_minutos>  |
    Y el historial de alertas indica que el paciente ha confirmado al menos el 80% de las tomas
    Cuando el médico decide evaluar el tratamiento actual
    Entonces si el paciente ha cumplido con el tratamiento anterior
    Y se decide modificar el tratamiento
    Entonces el sistema debe sugerir:
      | Tipo tratamiento    | Intensivo y preventivo   |
      | Medicación          | Triptanes + preventivos  |
      | Frecuencia          | Diaria (preventivo)      |
      | Recomendaciones     | Derivación a especialista|
    Pero si el paciente ha confirmado menos del 80% de las tomas
    Entonces se debe cancelar el tratamiento actual
    Y registrar el motivo como "incumplimiento de tratamiento"


  Escenario: Seguimiento de tratamiento para paciente femenino
    Dado que el paciente tiene un tratamiento activo de un episodio
    Y se verifican el historial del o los episodios con las siguientes características:
      | Característica           | Valor                    |
      | Duración Cefalea (horas) | <duracion_cefalea_horas> |
      | Severidad del Dolor      | <severidad>              |
      | Localización del Dolor   | <localizacion>           |
      | Carácter del Dolor       | <caracter_dolor>         |
      | Empeora con Actividad    | <empeora_actividad>      |
      | Náuseas o Vómitos        | <nauseas_vomitos>        |
      | Sensibilidad a la Luz    | <fotofobia>              |
      | Sensibilidad al Sonido   | <fonofobia>              |
      | Presencia de Aura        | <presencia_aura>         |
      | Síntomas del Aura        | <sintomas_aura>          |
      | Duración del Aura (min)  | <duracion_aura_minutos>  |
      | En menstruación          | <en_menstruacion>        |
      | Anticonceptivos          | <anticonceptivos>        |
    Y el historial de alertas indica que el paciente ha confirmado al menos el 80% de las tomas
    Cuando el médico decide evaluar el tratamiento actual
    Entonces si el paciente ha cumplido con el tratamiento anterior
    Y se decide modificar el tratamiento
    Entonces el sistema debe sugerir:
      | Tipo tratamiento    | Intensivo y preventivo   |
      | Medicación          | Triptanes + preventivos  |
      | Frecuencia          | Diaria (preventivo)      |
      | Recomendaciones     | Derivación a especialista|
    Pero si el paciente ha confirmado menos del 80% de las tomas
    Entonces se debe cancelar el tratamiento actual
    Y registrar el motivo como "incumplimiento de tratamiento"