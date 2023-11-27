import os
import boto3
from botocore.exceptions import NoCredentialsError

from app.config.setting import settings

def get_s3():
    s3 = boto3.client('s3', region_name=settings.aws_region,
                      aws_access_key_id=settings.aws_access_key_id,
                      aws_secret_access_key=settings.aws_secret_access_key)

    return s3

def upload_file_to_s3(local_file_path, bucket_name, s3_file_name=None, ):
    if s3_file_name is None:
        s3_file_name = os.path.basename(local_file_path)

    try:
        s3 = get_s3()
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print(f"File '{local_file_path}' uploaded to '{bucket_name}' as '{s3_file_name}'")
    except FileNotFoundError:
        print(f"The file '{local_file_path}' was not found.")
    except NoCredentialsError:
        print("Credentials not available.")


def upload_folder_to_s3(local_folder_path, bucket_name, given_file_name=""):
    s3_file_list =[]
    try:
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)

                # Get the last folder name from the local file path
                last_folder_name = os.path.basename(os.path.dirname(local_file_path))

                # Create the S3 file name
                s3_file_name = f"{last_folder_name}_{given_file_name}/{file}"

                # Convert path separators to '/'
                s3_file_name = s3_file_name.replace(os.path.sep, '/')

                # Upload the file to S3
                upload_file_to_s3(local_file_path, bucket_name, s3_file_name)
                s3_file_list.append(s3_file_name)
    except NoCredentialsError:
        print("Credentials not available.")

    return s3_file_list

