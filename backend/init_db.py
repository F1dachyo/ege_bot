from sqlalchemy import create_engine, Column, Integer, String, UUID, Date, DateTime, Boolean, ARRAY, JSON
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine('postgresql+psycopg://admin:7465@localhost:5432/uchi_bot')
session = Session(engine)

class Ex4(Base):
    __tablename__ = 'ex4'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    prompt = Column(String)
    tokens = Column(ARRAY(JSON), nullable=False)
    answers = Column(ARRAY(JSON), nullable=False)
    is_hard = Column(Boolean, nullable=False)
    comment = Column(String)

class Ex9(Base):
    __tablename__ = 'ex9'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    prompt = Column(String)
    tokens = Column(ARRAY(JSON), nullable=False)
    answers = Column(ARRAY(JSON), nullable=False)
    is_hard = Column(Boolean, nullable=False)
    comment = Column(String, nullable=False)

Base.metadata.create_all(engine, tables=[Ex4.__table__, Ex9.__table__])