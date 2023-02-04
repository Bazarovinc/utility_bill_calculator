from src.data.base_repository import BaseRepository
from src.data.interfaces import IMeasurementsRepo, ITariffsRepo
from src.data.models import Measurements, Tariffs
from src.dto.output import MeasurementsOutSchema, TariffsOutSchema


class MeasurementsRepo(IMeasurementsRepo, BaseRepository[Measurements, MeasurementsOutSchema]):
    model = Measurements
    schema = MeasurementsOutSchema

    def delete(self, id: int) -> None:
        self._session.query(self.model).where(self.model.id == id).delete()
        self._session.commit()


class TariffsRepo(ITariffsRepo, BaseRepository[Tariffs, TariffsOutSchema]):
    model = Tariffs
    schema = TariffsOutSchema
