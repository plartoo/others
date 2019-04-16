import os

from azure.storage.blob import BlockBlobService

from account_info import *


def list_blob_names(container_name, dir="", delimiter=""):
    """
    REF: https://stackoverflow.com/a/51145632
    :param container_name: name of container (str)
    :param virtualdir: path (e.g., "dir1/dir2/" of blob's virtual director
    :param delimiter:
    :return:
    """
    block_blob_service = BlockBlobService(account_name=BLOB_STORAGE_ACCOUNT_NAME,
                                          account_key=BLOB_STORAGE_ACCOUNT_KEY)
    blob_content_generator = block_blob_service.list_blobs(container_name, prefix=dir, delimiter=delimiter)
    return [blob.name for blob in blob_content_generator]


def list_file_names(container_name):
    blob_names = list_blob_names(container_name)
    return list(map(os.path.basename, blob_names))


def download_blob_file_to_local_folder(container_name, blob_file_with_path, local_file_with_path):
    block_blob_service = BlockBlobService(account_name=BLOB_STORAGE_ACCOUNT_NAME,
                                          account_key=BLOB_STORAGE_ACCOUNT_KEY)
    block_blob_service.get_blob_to_path(container_name, blob_file_with_path, local_file_with_path)
    print("\nDownloaded:", blob_file_with_path, "and placed it here:", local_file_with_path)


def upload_from_local_to_blob(container_name, local_file_path_and_name, dest_blob_path_and_name):
    block_blob_service = BlockBlobService(account_name=BLOB_STORAGE_ACCOUNT_NAME,
                                          account_key=BLOB_STORAGE_ACCOUNT_KEY)
    block_blob_service.create_blob_from_path(container_name,
                                             dest_blob_path_and_name,
                                             local_file_path_and_name)
    print("\nUploaded local file:", local_file_path_and_name, "\nand placed it here:", dest_blob_path_and_name)
