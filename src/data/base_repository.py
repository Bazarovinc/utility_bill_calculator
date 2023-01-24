from typing import Generic, Type, TypeVar

from pydantic.main import BaseModel
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from src.data.database import Base, SessionManager
from src.data.interfaces import IRepository

ModelType = TypeVar("ModelType", bound=Base)
OutSchema = TypeVar("OutSchema", bound=BaseModel)


class BaseRepository(IRepository, Generic[ModelType, OutSchema]):
    model: Type[ModelType]
    schema: Type[OutSchema]

    def __init__(self, session: Session) -> None:
        self._session: Session = session

    def get_last_created(self) -> OutSchema:
        return self.schema.from_orm(
            self._session.query(self.model).order_by(desc(self.model.created_at)).first()
        )

    def create(self, data: dict) -> OutSchema:
        obj = self.model(**data)
        self._session.add(obj)
        self._session.flush()
        return self.schema.from_orm(
            self._session.query(self.model).where(self.model.id == obj.id).one()
        )
