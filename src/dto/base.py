from pydantic import BaseModel


class OrmMode(BaseModel):
    class Config:
        orm_mode = True
