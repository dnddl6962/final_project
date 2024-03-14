import os
import dotenv
import boto3
import json

# AWS 계정 자격 증명 및 리전 설정
env_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_path)

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
region_name = 'ap-northeast-2'

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)


# S3 버킷과 파일 이름 설정
bucket_name = 'mathcat-bucket'
object_key = 'irt_result/yyyy=2024/mm=03/dd=13/irt_result.json'


def load_data(bucket_name, object_key):

    # JSON 파일 읽어오기
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))
        return json_data
    
    except Exception as e:
        print(e)