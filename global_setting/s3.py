import boto3
from setting import bucket_name
s3 = boto3.resource('s3')


def upload_file(local_path, s3_path):
    """
    upload a file to s3
    :param local_path: string-> the loc of your file in the local pc
    :param s3_path: string -> the loc you want to upload to s3
    :return: None
    """
    with open(local_path, 'rb') as binary_data:
        s3.Bucket(bucket_name).put_object(Key=s3_path, Body=binary_data)


def download_file(s3_path, local_path):
    """
    download a file from s3
    :param s3_path: string -> the loc of the file in s3
    :param local_path: string -> where you want to download the file
    :return: None
    """
    s3.meta.client.download_file(bucket_name, s3_path, local_path)
