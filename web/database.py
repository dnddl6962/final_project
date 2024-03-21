from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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