import os

from boto3 import client, resource
import botocore

from s3_account_info import *


def list_key_names(folder):
    """
    :return: A list of S3 keys such as ['Facebook/websales_20161202.csv', ...]
    """
    key_names = []

    s3 = client('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
    for key in s3.list_objects(Bucket=S3_BUCKET, Prefix=folder)['Contents']:
        name = str(key['Key'])
        if name != folder:
            key_names.append(name)
    return key_names


def list_file_names(folder):
    key_names = list_key_names(folder)
    return list(map(os.path.basename, key_names))


def download_from_s3(s3_source_path_and_file_str, dest_path_and_file_str):
    # Download file: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html
    s3 = resource('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)
    try:
        s3.Bucket(S3_BUCKET).download_file(s3_source_path_and_file_str, dest_path_and_file_str)
        print("\nDownloaded s3 source:", s3_source_path_and_file_str, "\nand placed it here:", dest_path_and_file_str)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def archive_files(from_folder, to_folder, new_file_postfix=''):
    print("Archiving files within S3 folder:", from_folder)
    for f_name in list_file_names(from_folder):
        source_key = from_folder + f_name
        f_name_without_extension = os.path.splitext(f_name)[0]
        f_extension = os.path.splitext(f_name)[1]
        dest_key = to_folder + f_name_without_extension + new_file_postfix + f_extension

        archive_file(source_key, dest_key)


def archive_file(source_key, dest_key):
    s3 = resource('s3', aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

    s3.Object(S3_BUCKET, dest_key).copy_from(CopySource={'Bucket': S3_BUCKET, 'Key': source_key})
    print("Deleting:", source_key)

    s3.Object(S3_BUCKET, source_key).delete()
    print("Archived this key:\t", source_key, "\tto\t", dest_key)
