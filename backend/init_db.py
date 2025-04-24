from sqlalchemy import create_engine, Column, Integer, String, UUID, Date, DateTime, Boolean, ARRAY, JSON
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()
engine = create_engine('postgresql+psycopg://admin:7465@localhost:5432/uchi_bot')
session = Session(engine)

class User(Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)
    streak = Column(Integer, nullable=False)
    all_answers = Column(Integer, nullable=False)
    right_answers = Column(Integer, nullable=False)
    date_last_update_streak = Column(Date, nullable=False)

class UsersMistakes(Base):
    __tablename__ = 'users_mistakes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    task_id = Column(Integer, nullable=False)
    task_type = Column(Integer, nullable=False)

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

class Ex10(Base):
    __tablename__ = 'ex10'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    prompt = Column(String)
    tokens = Column(ARRAY(JSON), nullable=False)
    answers = Column(ARRAY(JSON), nullable=False)
    is_hard = Column(Boolean, nullable=False)
    comment = Column(String, nullable=False)

class Ex11(Base):
    __tablename__ = 'ex11'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    prompt = Column(String)
    tokens = Column(ARRAY(JSON), nullable=False)
    answers = Column(ARRAY(JSON), nullable=False)
    is_hard = Column(Boolean, nullable=False)
    comment = Column(String, nullable=False)

class Ex12(Base):
    __tablename__ = 'ex12'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    prompt = Column(String)
    tokens = Column(ARRAY(JSON), nullable=False)
    answers = Column(ARRAY(JSON), nullable=False)
    is_hard = Column(Boolean, nullable=False)
    comment = Column(String, nullable=False)

Base.metadata.create_all(engine, tables=[User.__table__, UsersMistakes.__table__, Ex4.__table__, Ex9.__table__, Ex10.__table__, Ex11.__table__, Ex12.__table__])