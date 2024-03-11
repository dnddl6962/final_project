import boto3
import json
from datetime import datetime


# S3 클라이언트 생성
s3 = boto3.client('s3')

batch_date = datetime.now().strftime('%Y%m%d')

_y = batch_date[:4]
_m = batch_date[4:6]
_d = batch_date[6:]

file_path = './test-2pl/best_parameters.json'

with open(file_path, 'r') as f:
    data = json.load(f)


# JSON 데이터를 문자열로 변환
json_data = json.dumps(data)

# 파일을 S3 버킷에 업로드
bucket_name = 'mathcat-bucket'
file_name = f'irt_result/yyyy={_y}/mm={_m}/dd={_d}/irt_result.json'  # S3에 저장될 파일 이름
s3.put_object(Bucket=bucket_name, Key=file_name, Body=json_data)

print(f'{file_name} has been uploaded to {bucket_name}')
