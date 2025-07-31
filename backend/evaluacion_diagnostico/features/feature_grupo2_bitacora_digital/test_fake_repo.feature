# language: es
Característica: Prueba del repositorio fake con modelos reales
  Como desarrollador
  Quiero probar que el repositorio fake funciona con modelos reales
  Para asegurar que el patrón funciona igual que en el ejemplo

  Escenario: Crear paciente con repositorio fake
    Dado que existe un paciente con email "test@example.com" y nombre "Juan Pérez"
    Cuando se registra una nueva entrada en la bitácora
    Entonces el sistema debe almacenar la información correctamente
