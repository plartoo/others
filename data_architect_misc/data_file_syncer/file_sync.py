"""
Script to copy files from/to local computer folder and Azure blob.
Use this script to sync files between local folder and Azure blob.

Notes:
1) This script only runs on local computer
(that is, it is not designed to be embedded in cloud VMs
like Azure Batch instances).

2) This script expects user to either provide Azure storage
account key as argument or set it as an environment variable
with the variable name, STORAGE_ACCOUNT_KEY, in local machine.

To set environment variable in Windows, one needs to
enter this command below in command prompt:
> setx STORAGE_ACCOUNT_KEY <azure storage account key>

To set environment variable in Mac or Unix, enter this in
command prompt (e.g., Bash):
> export STORAGE_ACCOUNT_KEY=<azure storage account key>
or embed it in one's user profile such as ~/.bash_profile.
For more, Google how to set environment variables in
corresponding OS that the user is running this script on.

Author: Phyo Thiha
Development Started: Sep 10, 2020
"""
import argparse
import fnmatch
import json
import os

from azure.storage.blob import BlobServiceClient

DESC = """
Script to copy files from/to local computer folder and Azure blob.
Use this script to sync files between local folder and Azure blob.

Usage examples:
1) If the STORAGE_ACCOUNT_KEY environment variable 
is set with Azure blob storage account's key, do this:
> python file_sync.py -c sync_config.json

2) If the STORAGE_ACCOUNT_KEY environment variable 
is NOT set, but the user wants to provide it via command 
prompt, do this:
> python file_sync.py -c sync_config.json -k <azure storage account key>

In both of the above use cases, 'sync_config.json' is 
the JSON file that tells this script where to copy 
the files from and where to send them as final destination. 

TODO: explain how to write config file. 
"""


def get_list_files_in_folder(path_of_local_folder):
    # REF: https://stackoverflow.com/a/3207973
    return [f for f in os.listdir(path_of_local_folder)
            if os.path.isfile(os.path.join(path_of_local_folder, f))]


def get_list_of_files_in_blob_path(container_client, blob_path):
    # https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.containerclient?view=azure-python#list-blobs-name-starts-with-none--include-none----kwargs-
    return [b for b in container_client.list_blobs(name_starts_with=blob_path)]


def are_both_keys_in_dict(dictionary, k1, k2):
    # REF: https://stackoverflow.com/a/1285920
    return all(k in dictionary for k in (k1, k2))


def main():
    # 0. Extract input parameters for the program
    parser = argparse.ArgumentParser(
        description=DESC,
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)
    parser.add_argument('-c', type=str, required=True,
                        help="Provide JSON config file that tells this script "
                             "where to copy the files from and their destination"
                             "(blob location or just another local path).")
    parser.add_argument('-k', type=str,
                        help="Azure storage account's key. Only provide this "
                             "if the key is not set to environment variable, "
                             "STORAGE_ACCOUNT_KEY.")
    args = parser.parse_args()

    # 1. Read Azure storage account key
    if args.k:
        storage_accnt_key = args.k
    elif 'STORAGE_ACCOUNT_KEY' in os.environ:
        storage_accnt_key = os.environ.get('STORAGE_ACCOUNT_KEY')
    else:
        raise Exception("Azure storage account's key must be "
                        "provided as an argument to this program with 'k' flag or must "
                        "be set as an environment variable, 'STORAGE_ACCOUNT_KEY'.")

    # 2. Load config from JSON file
    with open(args.c) as f:
        sync_config = json.load(f)

    for config in sync_config:
        container_name = config['container_name']
        storage_accnt_url = config['storage_account_url']
        blob_service_client = BlobServiceClient(account_url=storage_accnt_url,
                                                credential=storage_accnt_key)
        container_client = blob_service_client.get_container_client(container_name)

        for c in config['files_to_copy']:
            if are_both_keys_in_dict(c, 'from_local_folder_path', 'to_blob_path'):
                files_to_copy = get_list_files_in_folder(c['from_local_folder_path'])
                files_in_destination = get_list_of_files_in_blob_path(container_client,
                                                                      c['to_blob_path'])
            elif are_both_keys_in_dict(c, 'from_blob_path', 'to_local_folder_path'):
                files_to_copy = get_list_of_files_in_blob_path(container_client,
                                                               c['from_blob_path'])
                files_in_destination = get_list_files_in_folder(c['to_local_folder_path'])






        # import pdb; pdb.set_trace()
        print("End of program.")


if __name__ == '__main__':
    main()
