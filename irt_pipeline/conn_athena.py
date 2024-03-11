from pyathena import connect
from pyathena.pandas.cursor import PandasCursor
import os
from log_data import setup_logging

logger = setup_logging()

def connect_to_athena():
    try:
        awsid =os.getenv('aws_access_key_id')
        awspassword = os.getenv('aws_secret_access_key')
        
        conn = connect(aws_access_key_id=awsid,
                       aws_secret_access_key=awspassword,
                       s3_staging_dir='s3://mathcat-bucket/BD5-Data/',
                       region_name='ap-northeast-2',
                       cursor_class=PandasCursor)
        logger.info("Successfully connected to Athena")
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to Athena: {str(e)}")
        raise e
