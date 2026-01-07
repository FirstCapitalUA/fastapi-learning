from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel

from core.config import settings

# для PostgreSQL:
# DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # только для SQLite
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
