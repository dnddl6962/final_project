from module import TitanicProcessor
import boto3
from sqlalchemy import create_engine
import pandas as pd
from io import StringIO
import os
# S3 클라이언트 생성
s3 = boto3.client('s3')
# ...

database_type = os.getenv('DATABASE_TYPE', 'mysql+pymysql')  # pymysql을 명시적으로 사용
username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
host = os.getenv('DATABASE_HOST')
port = os.getenv('DATABASE_PORT', '3306')  # MySQL의 기본 포트
database_name = os.getenv('DATABASE_NAME')

# SQLAlchemy 엔진 생성 시 pymysql을 명시적으로 사용
engine = create_engine(f"{database_type}://{username}:{password}@{host}:{port}/{database_name}")

# ...



# S3 버킷과 파일 키 설정
bucket_name = 'mathcat-bucket'
file_key = 'sample/titanic.csv'
obj = s3.get_object(Bucket=bucket_name, Key=file_key)
data = obj['Body'].read().decode('utf-8')



processor = TitanicProcessor(StringIO(data), "result.csv")
processor.process()

processor.df.to_sql('passengers', engine, if_exists='replace')  
