import os
import sys
import django

def before_all(context):
    """Configurar Django antes de ejecutar todos los tests"""
    print("🔧 Configurando Django para Behave...")
    
    # CRÍTICO: Configurar Django igual que en tu ejemplo que funciona
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'migraine_app.settings')
    
    # VERIFICAR si Django YA está configurado (evitar error "populate() isn't reentrant")
    from django.apps import apps
    
    if apps.ready:
        print("✅ Django YA está configurado - usando configuración existente")
    else:
        try:
            print("📋 Llamando a django.setup()...")
            django.setup()
            print("✅ Django configurado correctamente")
        except RuntimeError as e:
            if "populate() isn't reentrant" in str(e):
                print("✅ Django ya estaba configurado - continuando...")
            else:
                print(f"❌ Error configurando Django: {e}")
                raise
        except Exception as e:
            print(f"❌ Error configurando Django: {e}")
            print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
            print(f"Python path: {sys.path}")
            raise
    
    # VERIFICACIÓN FINAL
    if apps.ready:
        print("✅ Django apps están listas")
        print("🚀 Behave listo para ejecutar tests")
    else:
        print("❌ Django apps NO están listas")
        raise Exception("Django apps no están configuradas correctamente")