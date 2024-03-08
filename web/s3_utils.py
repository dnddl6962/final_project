# import boto3

# def save_results_to_s3(user_id, results):
#     s3 = boto3.client('s3')
#     bucket_name = 'your-bucket-name'
#     object_key = f'user_results/{user_id}.json'
#     s3.put_object(Body=str(results), Bucket=bucket_name, Key=object_key)
