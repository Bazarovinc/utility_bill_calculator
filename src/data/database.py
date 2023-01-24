import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DSN = "sqlite:///database"

engine = sqlalchemy.create_engine(DSN, pool_pre_ping=True)

SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class SessionManager:
    def __init__(self):
        self._session: Session = SessionLocal()

    def __enter__(self):
        return self._session

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._session.commit()
        self._session.close()
