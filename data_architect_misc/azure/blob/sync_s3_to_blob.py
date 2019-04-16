import os
import shutil
import uuid

import s3_utils
import azure_utils
import azure_file_utils

from account_info import *


def list_file_names(list_of_file_names_with_path):
    return list(map(os.path.basename, list_of_file_names_with_path))


def main():
    # 1. create local directory and append it to sys.path so that we can load Python modules in it later
    local_dir_name = str(uuid.uuid4())
    azure_file_utils.create_unique_local_download_directory(local_dir_name)

    #"""
    # The JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    json_activity = {'typeProperties': {'extendedProperties':
                                            {'s3_folder': 'digital/double_verify_iqpa/',
                                             'blob_container': 'pacing-report', 
                                             'blob_dir_path': 'dv-iqpa-test',
                                             }
                                        }
                     }
    """
    # 2a. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    """

    s3_folder = json_activity['typeProperties']['extendedProperties']['s3_folder']
    blob_container = json_activity['typeProperties']['extendedProperties']['blob_container']
    blob_dir_path = json_activity['typeProperties']['extendedProperties']['blob_dir_path']

    # 3. Get the files not in the blob but are in S3
    s3_file_names = s3_utils.list_key_names(s3_folder)
    blob_file_names = azure_utils.list_blob_names(blob_container, dir=blob_dir_path)
    file_difference_list = list(set(list_file_names(s3_file_names))
                                - set(list_file_names(blob_file_names)))

    # 4. Now, download the ones not yet in the blob (but in S3) to local folder
    local_files = []
    for f in file_difference_list:
        index = [i for i, s3f in enumerate(s3_file_names) if f in s3f]
        s3_file_with_path = s3_file_names[index[0]]
        local_file_with_path = os.path.join(local_dir_name, f)
        s3_utils.download_from_s3(s3_file_with_path, local_file_with_path)
        local_files.append(local_file_with_path)
    # 5. Upload the files that were just downloaded in the local folder to blob destination
    for f in local_files:
        local_file_name = os.path.basename(f)
        dest_blob_path_and_name = azure_file_utils.join_path_and_file_name(blob_dir_path,
                                                                           local_file_name,
                                                                           separator='/')
        azure_utils.upload_from_local_to_blob(blob_container, f, dest_blob_path_and_name)

    print("\nSynced files between S3 and Blob location")
    # 6. delete local files and folder downloaded temporarily from Azure
    try:
        shutil.rmtree(local_dir_name)
        print("\nDeleted local folder and its contents:", local_dir_name)
    except OSError as e:
        print("\nError: %s - %s." % (e.filename, e.strerror))


if __name__ == '__main__':
    main()
