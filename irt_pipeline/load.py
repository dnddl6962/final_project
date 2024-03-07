import boto3
from io import StringIO
import pandas as pd

def load_and_preprocess_data(bucket_name, file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    data = obj['Body'].read().decode('utf-8')
    data_io = StringIO(data)
    final_5g = pd.read_csv(data_io)
    
    df5 = final_5g[['userid', 'quizcode', 'correct']]
    df5['correct'] = df5['correct'].replace({'O': 1, 'X': 0})
    df5.columns = ['UserID', 'QuizCode', 'Correct']
    
    return df5
