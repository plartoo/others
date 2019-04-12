import pdb
import os

import s3_utils
import azure_utils

from account_info import *


def list_file_names(list_of_file_names_with_path):
    return list(map(os.path.basename, list_of_file_names_with_path))


s3_folder = 'digital/double_verify_iqpa/'
blob_container = 'pacing-report'

s3_file_names = s3_utils.list_key_names(s3_folder)
blob_file_names = azure_utils.list_blob_names(blob_container)
file_difference_list = list(set(list_file_names(s3_file_names)) - set(list_file_names(blob_file_names)))

# Download file: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html


pdb.set_trace()
print('done')