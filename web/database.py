from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import dotenv

# AWS 계정 자격 증명 및 리전 설정
env_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_path)

host = os.environ.get("AWS_RDS_HOST")
port = os.environ.get("AWS_RDS_PORT")
user_name = os.environ.get("AWS_RDS_USERNAME")
password = os.environ.get("AWS_RDS_PASSWORD")

DATABASE_URL = f"mysql+pymysql://{user_name}:{password}@{host}:{port}/dbtest"
engine = create_engine(DATABASE_URL, connect_args={'connect_timeout': 10})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# def create_tables():
#     Base.metadata.create_all(bind=engine)
#     print("Tables created successfully")

# 사용자 ID 중복 확인 함수
def check_userid_duplicate(userid: str) -> bool:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM id_test WHERE userid = :userid"),
            {'userid': userid}
        ).fetchone()
        return result is not None