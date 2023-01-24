from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar

from pydantic.main import BaseModel

OutSchema = TypeVar("OutSchema", bound=BaseModel)


class IRepository(ABC):
    @abstractmethod
    def get_last_created(self) -> OutSchema:
        ...

    @abstractmethod
    def create(self, data: dict) -> OutSchema:
        ...


class IMeasurementsRepo(IRepository):
    @abstractmethod
    def delete(self, id: int) -> None:
        ...


class ITariffsRepo(IRepository):
    ...
