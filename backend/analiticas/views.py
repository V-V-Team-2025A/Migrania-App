# analiticas/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import AnalisisPatronesService
from .repositories import DjangoAnalisisPatronesRepository
from .serializers import AnalisisPatronesSerializer

class AnalisisPatronesView(APIView):
    permission_classes = [IsAuthenticated] # Solo usuarios autenticados pueden ver su análisis

    def get(self, request, *args, **kwargs):
        # 1. Obtener el ID del paciente del usuario autenticado
        paciente_id = request.user.pk

        # 2. Inyectar el repositorio REAL en el servicio
        repo = DjangoAnalisisPatronesRepository()
        servicio_analisis = AnalisisPatronesService(repository=repo)

        # 3. Ejecutar todos los métodos de análisis
        resultados = {
            "conclusion_clinica": servicio_analisis.analizar_patrones_clinicos(paciente_id),
            "conclusiones_sintomas": servicio_analisis.analizar_frecuencia_sintomas(paciente_id),
            "conclusion_aura": servicio_analisis.analizar_patrones_aura(paciente_id),
            "dias_recurrentes": servicio_analisis.analizar_recurrencia_semanal(paciente_id),
            "conclusion_hormonal": servicio_analisis.analizar_patron_menstrual(paciente_id),
        }

        # 4. Usar el serializador para formatear la respuesta
        serializer = AnalisisPatronesSerializer(data=resultados)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)