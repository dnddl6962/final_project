from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class StudentTest(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student = Column(String(4000), index=True)
    quizcode = Column(Integer)
    correct = Column(String(100))
    no = Column(Integer)
    datetime = Column(DateTime, default=datetime.utcnow)
