from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

# host = os.environ.get("AWS_RDS_HOST")
# port = os.environ.get("AWS_RDS_PORT")
# user_name = os.environ.get("AWS_RDS_USERNAME")
# password = os.environ.get("AWS_RDS_PASSWORD")


DATABASE_URL= "mysql+pymysql://dbtest:shinemathcat@database-1.c1oby0nabaqs.ap-northeast-2.rds.amazonaws.com:3306/dbtest"

#f"mysql+pymysql://{user_name}:{password}@{host}:{port}/dbtest"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")