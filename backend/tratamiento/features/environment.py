import os
import django
import random
from faker import Faker

def before_all(context):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "migraine_app.settings")
    django.setup()
    Faker.seed(12345)
    random.seed(12345)

def before_scenario(context, scenario):
    from tratamiento.repositories import FakeTratamientoRepository
    from tratamiento.tratamiento_service import TratamientoService
    from tratamiento.medicamento_service import MedicamentoService

    context.tratamiento_repository = FakeTratamientoRepository()
    context.tratamiento_service = TratamientoService(context.tratamiento_repository)
    context.medicamento_service = MedicamentoService(context.tratamiento_repository)
