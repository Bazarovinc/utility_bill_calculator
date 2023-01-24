from sqlalchemy import func
from sqlalchemy.orm import Session

from src.data.models import Measurements, Tariffs
from src.dto.app_schemas import MeasurementsSchema, TariffsSchema


def get_current_tariffs(session: Session) -> TariffsSchema:
    return TariffsSchema.from_orm(session.query(Tariffs).where(func.max(Tariffs.created_at)).one())


def get_last_measurements(session: Session) -> MeasurementsSchema:
    return MeasurementsSchema.from_orm(
        session.query(Measurements).where(func.max(Measurements.created_at)).one()
    )


def create_new_measurements(session: Session, data: dict) -> None:
    data_model = Measurements(**data)
    session.add(data_model)
