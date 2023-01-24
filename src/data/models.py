from datetime import datetime
from decimal import Decimal

import sqlalchemy.types as types
from sqlalchemy import Column, Integer, func
from sqlalchemy.dialects.sqlite import DATETIME

from src.data.database import Base
from src.dto.types import ElectricityMeasurement, Money, Month, WaterMeasurement


class SqliteNumeric(types.TypeDecorator):
    impl = types.String

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(types.VARCHAR(100))

    def process_bind_param(self, value, dialect):
        return str(value)

    def process_result_value(self, value, dialect):
        return Decimal(value)


class MoneySqlite(SqliteNumeric):
    def process_result_value(self, value, dialect):
        return Money(round(Decimal(value), 2))


class WaterMeasurementSqlite(SqliteNumeric):
    def process_result_value(self, value, dialect):
        return WaterMeasurement(round(Decimal(value), 3))


class ElectricityMeasurementSqlite(SqliteNumeric):
    def process_result_value(self, value, dialect):
        return ElectricityMeasurement(round(Decimal(value), 2))


class Measurements(Base):

    __tablename__ = "measurements"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    month: Month = Column(Integer, index=True)
    year: int = Column(Integer, index=True)
    cold_measurement: WaterMeasurement = Column(WaterMeasurementSqlite, unique=True)
    hot_measurement: WaterMeasurement = Column(WaterMeasurementSqlite, unique=True)
    electricity_measurement: ElectricityMeasurement = Column(
        ElectricityMeasurementSqlite, unique=True
    )
    created_at: datetime = Column(
        DATETIME,
        server_default=func.now(),
    )


class Tariffs(Base):

    __tablename__ = "tariffs"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    cold_tariff: Money = Column(MoneySqlite)
    hot_tariff: Money = Column(MoneySqlite)
    electricity_tariff: Money = Column(MoneySqlite)
    created_at: datetime = Column(
        DATETIME,
        server_default=func.now(),
    )
