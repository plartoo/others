"""
Script to upload/download files between local computer
and/or Azure blob.

Notes:
1) This script only runs on local computer
(that is, it is not designed to be embedded in cloud VMs
like Azure Batch instances).

2) This script expects user to either provide Azure storage
account key as argument to the script or set it as an
environment variable with variable name, STORAGE_ACCOUNT_KEY,
in the local machine.

To set environment variable in Windows, one needs to
enter this command below in command prompt:
> setx STORAGE_ACCOUNT_KEY <azure storage account key>

To set environment varaible in Mac or Unix command line
interface:
> export STORAGE_ACCOUNT_KEY=<azure storage account key>
or embed it in one's user profile such as ~/.bash_profile.
For more, Google how to set environment variables in
corresponding OS that the user is running this script on.

Author: Phyo Thiha
Last Modified: Sep 10, 2020
"""
import argparse
import fnmatch
import json
import os

from azure.storage.blob import BlobServiceClient

DESC = """
This script is used to keep files synced between 
our team's local machine folders and Azure blob 
where we ultimately store our data files.

Run this script periodically (preferably every time 
you have processed/transformed data for individual 
country) to keep files synced between local and Azure 
blob. 

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

    storage_accnt_url = sync_config['storage_account_url']
    blob_service_client = BlobServiceClient(account_url=storage_accnt_url,
                                            credential=storage_accnt_key)
    # import pdb; pdb.set_trace()
    print("End of program.")


if __name__ == '__main__':
    main()
