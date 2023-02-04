from dependency_injector import containers, providers

from src.data.database import get_session
from src.data.repositories import MeasurementsRepo, TariffsRepo
from src.use_case import UseCase


class Container(containers.DeclarativeContainer):
    session = providers.Resource(get_session)
    measurements_repo = providers.Singleton(MeasurementsRepo, session=session)
    tariffs_repo = providers.Singleton(TariffsRepo, session=session)
    use_case = providers.Singleton(
        UseCase, measurements_repo=measurements_repo, tariffs_repo=tariffs_repo
    )
