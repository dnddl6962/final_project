from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
#load_dotenv()

# host = os.environ.get("AWS_RDS_HOST")
# #port = os.environ.get("AWS_RDS_PORT")
# user_name = os.environ.get("AWS_RDS_USERNAME")
# password = os.environ.get("AWS_RDS_PASSWORD")


database_type = os.getenv('DATABASE_TYPE', 'mysql+pymysql')  # pymysql을 명시적으로 사용
username = os.getenv('AWS_RDS_USERNAME')
password = os.getenv('AWS_RDS_PASSWORD')
host = os.getenv('AWS_RDS_HOST')
port = os.getenv('AWS_RDS_PORT', '3306')  # MySQL의 기본 포트
database_name = os.getenv('DATABASE_NAME')
# SQLAlchemy 엔진 생성 시 pymysql을 명시적으로 사용
engine = create_engine(f"{database_type}://{username}:{password}@{host}:{port}/{database_name}")


#DATABASE_URL= f"mysql+pymysql://{user_name}:{password}@{host}:3306/dbtest"
#"mysql+pymysql://dbtest:shinemathcat@database-1.c1oby0nabaqs.ap-northeast-2.rds.amazonaws.com:3306/dbtest"


#engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 10})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")