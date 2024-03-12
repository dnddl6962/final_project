from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Nickname(Base):
    __tablename__ = 'nicknames'
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True)
