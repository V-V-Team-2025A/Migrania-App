# features/environment.py
from faker import Faker

def before_scenario(context, scenario):
    Faker.seed(1234)
    context.fake = Faker('es_ES')

    from usuarios.repositories import FakeUserRepository
    from tratamiento.repositories import FakeTratamientoRepository
    from tratamiento.tratamiento_service import TratamientoService
    from tratamiento.medicamento_service import MedicamentoService
    from evaluacion_diagnostico.repositories import FakeEpisodioCefaleaRepository
    from evaluacion_diagnostico.episodio_cefalea_service import EpisodioCefaleaService

    # Repositorios fakes
    context.user_repo = FakeUserRepository()
    context.trat_repo = FakeTratamientoRepository()
    context.epi_repo = FakeEpisodioCefaleaRepository()

    # Servicios
    context.trat_service = TratamientoService(context.trat_repo)
    context.med_service = MedicamentoService(context.trat_repo)
    context.epi_service = EpisodioCefaleaService(context.epi_repo)

def after_scenario(context, scenario):
    # Limpieza opcional si tus repos fakes tienen reset()
    for repo_name in ["user_repo", "trat_repo", "epi_repo"]:
        repo = getattr(context, repo_name, None)
        if repo and hasattr(repo, "reset"):
            repo.reset()
