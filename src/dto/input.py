from datetime import datetime

from pydantic import validator
from pydantic.main import BaseModel

from src.dto.types import ElectricityMeasurement, Money, Month, WaterMeasurement


class MeasurementsInSchema(BaseModel):
    month: Month
    year: int
    cold_measurement: WaterMeasurement
    hot_measurement: WaterMeasurement
    electricity_measurement: ElectricityMeasurement
    created_at: datetime = None

    @validator("created_at", pre=True, always=True)
    def set_last_update(cls, value: datetime | None) -> datetime:
        return value if value else datetime.now()


class TariffsInSchema(BaseModel):
    cold_tariff: Money
    hot_tariff: Money
    electricity_tariff: Money
    created_at: datetime = None

    @validator("created_at", pre=True, always=True)
    def set_last_update(cls, value: datetime | None) -> datetime:
        return value if value else datetime.now()
