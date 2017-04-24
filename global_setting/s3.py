import boto3
from setting import bucket_name
s3 = boto3.resource('s3')


def upload_file(local_path, s3_path):
    with open(local_path, 'rb') as binary_data:
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=binary_data)


def download_file(s3_path, local_path):
    s3.meta.client.download_file(bucket_name, s3_path, local_path)
