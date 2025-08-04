# citas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CitaViewSet, RecordatorioViewSet, UtilsViewSet

# Configurar el router de DRF
router = DefaultRouter()
router.register(r'citas', CitaViewSet, basename='cita')
router.register(r'recordatorios', RecordatorioViewSet, basename='recordatorio')
router.register(r'utils', UtilsViewSet, basename='utils')

urlpatterns = [
    # URLs del router
    path('', include(router.urls)),
]

"""
URLs disponibles:

CITAS:
- GET    /api/citas/                     # Listar citas (con filtros)
- POST   /api/citas/                     # Crear nueva cita
- GET    /api/citas/{id}/                # Detalle de cita específica
- PUT    /api/citas/{id}/                # Actualizar cita completa
- PATCH  /api/citas/{id}/                # Actualizar cita parcial
- DELETE /api/citas/{id}/                # Eliminar cita (solo admin)

ACCIONES PERSONALIZADAS DE CITAS:
- POST   /api/citas/urgente/             # Crear cita urgente
- GET    /api/citas/horarios_disponibles/ # Obtener horarios disponibles
- POST   /api/citas/{id}/reprogramar/    # Reprogramar cita específica
- POST   /api/citas/{id}/cancelar/       # Cancelar cita específica
- GET    /api/citas/mis_citas/           # Obtener citas del usuario autenticado
- GET    /api/citas/estadisticas/        # Estadísticas de citas (solo admin)
- GET    /api/citas/urgentes/            # Listar citas urgentes

RECORDATORIOS:
- GET    /api/recordatorios/             # Listar recordatorios
- POST   /api/recordatorios/             # Crear nuevo recordatorio
- GET    /api/recordatorios/{id}/        # Detalle de recordatorio específico
- PUT    /api/recordatorios/{id}/        # Actualizar recordatorio completo
- PATCH  /api/recordatorios/{id}/        # Actualizar recordatorio parcial
- DELETE /api/recordatorios/{id}/        # Eliminar recordatorio

ACCIONES PERSONALIZADAS DE RECORDATORIOS:
- GET    /api/recordatorios/mis_recordatorios/  # Recordatorios del usuario (pacientes)
- GET    /api/recordatorios/pendientes/         # Recordatorios pendientes (admin)
- POST   /api/recordatorios/{id}/marcar_enviado/ # Marcar como enviado
- POST   /api/recordatorios/procesar_pendientes/ # Procesar todos los pendientes

UTILIDADES:
- GET    /api/utils/opciones_discapacidad/      # Opciones de discapacidad
- GET    /api/utils/estados_cita/               # Estados disponibles para citas
- GET    /api/utils/tipos_recordatorio/         # Tipos de recordatorio
- GET    /api/utils/doctores_disponibles/       # Doctores disponibles por fecha/hora

EJEMPLOS DE USO:

1. Crear una cita:
POST /api/citas/
{
    "doctor_id": 1,
    "paciente_id": 2,
    "fecha": "2024-12-15",
    "hora": "09:00",
    "urgente": false,
    "motivo": "Consulta general"
}

2. Obtener horarios disponibles:
GET /api/citas/horarios_disponibles/?doctor_id=1&fecha=2024-12-15

3. Reprogramar cita:
POST /api/citas/5/reprogramar/
{
    "nueva_fecha": "2024-12-16",
    "nueva_hora": "10:00",
    "motivo": "Cambio de horario solicitado"
}

4. Crear cita urgente:
POST /api/citas/urgente/
{
    "paciente_id": 2,
    "motivo": "Dolor intenso en el pecho"
}

5. Listar citas con filtros:
GET /api/citas/?estado=pendiente&urgente=true&fecha=2024-12-15

6. Obtener mis citas (usuario autenticado):
GET /api/citas/mis_citas/

7. Crear recordatorio:
POST /api/recordatorios/
{
    "paciente_id": 2,
    "fecha": "2024-12-14",
    "hora": "18:00",
    "mensaje": "Recordatorio de cita médica mañana",
    "tipo": "cita_proxima"
}

8. Obtener doctores disponibles:
GET /api/utils/doctores_disponibles/?fecha=2024-12-15&hora=09:00
"""