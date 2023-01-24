from pydantic import ConstrainedDecimal, ConstrainedInt


class Month(ConstrainedInt):
    ge = 1
    le = 12


class Money(ConstrainedDecimal):
    decimal_places: int = 2
    max_digits: int = 15


class WaterMeasurement(ConstrainedDecimal):
    decimal_places: int = 3
    max_digits: int = 8


class ElectricityMeasurement(ConstrainedDecimal):
    decimal_places: int = 2
    max_digits: int = 8
