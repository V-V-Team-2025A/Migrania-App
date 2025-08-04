# analiticas/urls.py
from django.urls import path
from .views import AnalisisPatronesView

urlpatterns = [
    path('patrones/', AnalisisPatronesView.as_view(), name='analisis-patrones'),
]