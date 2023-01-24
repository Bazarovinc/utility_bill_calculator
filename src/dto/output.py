from src.dto.base import OrmMode
from src.dto.types import ElectricityMeasurement, Money, WaterMeasurement


class MeasurementsOutSchema(OrmMode):
    id: int
    month: int
    year: int
    cold_measurement: WaterMeasurement
    hot_measurement: WaterMeasurement
    electricity_measurement: ElectricityMeasurement


class TariffsOutSchema(OrmMode):
    id: int
    cold_tariff: Money
    hot_tariff: Money
    electricity_tariff: Money
