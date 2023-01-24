from src.data.database import SessionManager
from src.data.repositories import MeasurementsRepo, TariffsRepo
from src.use_case import UseCase

if __name__ == "__main__":
    with SessionManager() as session:
        measurements_repo = MeasurementsRepo(session)
        tariffs_repo = TariffsRepo(session)
        use_case = UseCase(measurements_repo, tariffs_repo)
        use_case.run()
