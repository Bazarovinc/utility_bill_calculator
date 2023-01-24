from decimal import Decimal

from pydantic import BaseModel, Field

from src.constants import MONTHS
from src.dto.types import ElectricityMeasurement, Money, Month, WaterMeasurement


class TraitInfo(BaseModel):
    trait_now: Decimal
    trait_last_month: Decimal
    tariff: Money
    round_arg: int = Field(default=2)

    @property
    def result(self) -> Decimal:
        return self.tariff * (self.trait_now - self.trait_last_month)

    @property
    def result_readable(self) -> str:
        return (
            f"({round(self.trait_now, self.round_arg)} - "
            f"{round(self.trait_last_month, self.round_arg)}) * "
            f"{round(self.tariff, 2)} = {round(self.result, 2)}"
        )


class WaterTraitInfo(TraitInfo):
    round_arg: int = 3


class Traits(BaseModel):
    cold_trait: WaterTraitInfo
    hot_trait: WaterTraitInfo
    electric_trait: TraitInfo
    months: list[Month]

    @property
    def pay_result(self) -> Decimal:
        return self.cold_trait.result + self.hot_trait.result + self.electric_trait.result

    @property
    def result_readable(self) -> str:
        return (
            f"{round(self.cold_trait.result, 2)} + "
            f"{round(self.hot_trait.result, 2)} + "
            f"{round(self.electric_trait.result, 2)} = "
            f"{round(self.pay_result, 2)}"
        )

    @property
    def months_readable(self) -> str:
        return " ".join([MONTHS[month] for month in self.months])


class AppInputSchema(BaseModel):
    cold_tariff: Money | None
    hot_tariff: Money | None
    electricity_tariff: Money | None
    cold_measurement: WaterMeasurement | None
    hot_measurement: WaterMeasurement | None
    electricity_measurement: ElectricityMeasurement | None
