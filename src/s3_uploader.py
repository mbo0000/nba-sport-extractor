import boto3
from botocore.exceptions import ClientError
import logging
# import configparser
import json
import os

'TODO: maybe this should be handle by Airflow?'
class S3_UploadUtil:
    def __init__(self) -> None:
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
        self.access_key = os.getenv('AWS_ACCESS_KEY')
        self.secret = os.getenv('AWS_SECRET_KEY')

    def upload_data(self, data_obj, s3_name_key):

        s3_client = boto3.client(
            service_name            ='s3',
            region_name             = 'us-west-1',
            aws_access_key_id       = self.access_key,
            aws_secret_access_key   = self.secret
        )

        try:
            response = s3_client.put_object(
                    
                    # convert API response data into str
                    Body = str(json.dumps(data_obj))
                    # Body        = data_obj
                    , Bucket    = self.bucket_name
                    , Key       = s3_name_key
                ) 
        except ClientError as e:
            logging.error(e)