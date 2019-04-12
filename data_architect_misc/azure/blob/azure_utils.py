import os

from azure.storage.blob import BlockBlobService

from account_info import *


def list_blob_names(container_name):
    block_blob_service = BlockBlobService(account_name=BLOB_STORAGE_ACCOUNT_NAME,
                                          account_key=BLOB_STORAGE_ACCOUNT_KEY)
    blob_content_generator = block_blob_service.list_blobs(container_name)
    return [blob.name for blob in blob_content_generator]


def list_file_names(container_name):
    blob_names = list_blob_names(container_name)
    return list(map(os.path.basename, blob_names))


def join_path_and_file_name(path, file_name, separator=os.sep):
    # Note: I can combine the following lines into one line of code,
    # but I won't because of better readability
    normalized_path = os.path.normpath(path)
    file_name_with_path = os.path.join(normalized_path, file_name).split(os.sep)
    return separator.join(file_name_with_path)


def download_blob_file_to_local_folder(container_name, blob_file_with_path, local_file_with_path):
    block_blob_service = BlockBlobService(account_name=BLOB_STORAGE_ACCOUNT_NAME,
                                          account_key=BLOB_STORAGE_ACCOUNT_KEY)
    block_blob_service.get_blob_to_path(container_name, blob_file_with_path, local_file_with_path)
    print("\nDownloaded:", blob_file_with_path, "and placed it here:", local_file_with_path)