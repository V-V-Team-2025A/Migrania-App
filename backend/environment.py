import os
import sys
import django

def before_all(context):
    """
    Configurar Django antes de ejecutar todos los tests de Behave
    Este environment.py sirve para TODAS las apps del proyecto
    """
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'migraine_app.settings')
    
    # Verificar si Django ya está configurado (evitar error "populate() isn't reentrant")
    from django.apps import apps
    
    if not apps.ready:
        try:
            django.setup()
        except RuntimeError as e:
            if "populate() isn't reentrant" not in str(e):
                raise
    
    # Verificación final
    if not apps.ready:
        raise Exception("Django apps no están configuradas correctamente")