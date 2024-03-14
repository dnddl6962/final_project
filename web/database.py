from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

DATABASE_URL= "mysql+pymysql://dbtest:shinemathcat@database-1.c1oby0nabaqs.ap-northeast-2.rds.amazonaws.com:3306/dbtest"

engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 10})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")