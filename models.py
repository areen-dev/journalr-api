from sqlalchemy import Column, Integer, String

from database import Base


class Entry(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=False)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
