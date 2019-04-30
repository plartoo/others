"""
Last Modified: April 23, 2019
Author: Phyo Thiha
Description:
Script to read Gmail, scan for desired data email, extract data download URL,
download data using that URL, upload that data into Azure Blob, and remove
any breadcrumbs files (such as credentials, and code files temporarily
downloaded into Azure Batch node).

Note: This script is intended to be run in a node of Azure Batch process.
'*_account_info' files are removed from this repo for obvious reason.
Please create your own specific account info files for azure and gmail
before using this script.
"""

from datetime import datetime
import json
import os
import requests
import re
import shutil
import sys
import uuid

import usprogrammatic_gmail_account_info
import azure_utils
import file_and_sys_utils
import gmail_utils


def get_key_or_default_from_dict(d, k, default=''):
    if d.get(k) is None:
        return default
    return d.get(k)


def find_urls(pattern, s):
    return re.findall(pattern, s, re.S)


def find_ttd_report_url(preceding_str, mail_body):
    url_pattern = r'.*(https?://\S+)'
    pattern = ''.join([preceding_str, url_pattern])
    return find_urls(pattern, mail_body)


def clean_ttd_report_url(url):
    return url.replace('\\r\\n', '')


def main():
    # 1. Create local dir to save downloaded data file
    local_dir_base_name = str(uuid.uuid4())
    local_data_dir_name = ''.join(['data_',local_dir_base_name])
    local_data_dir = file_and_sys_utils.get_full_path(local_data_dir_name)
    file_and_sys_utils.create_unique_local_download_directory(local_data_dir)

    """
    # JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    json_activity = {
        'typeProperties':
            {
                'extendedProperties':
                    {
                        'blob_container': 'pacing-report', # required
                        'blob_upload_path': 'ttd', # required
                        'query':'in:inbox subject:Colgate Programmatic Phyo GroupM Redfuse newer_than:1d', # required
                        'file_type':'.xlsx', # required
                        'preceding_str':'clicking the link below', # optional
                        'output_file_name_prefix':'ttd_', # optional
                    }
            }
    }
    """

    # 2a. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    #"""
    blob_container = json_activity['typeProperties']['extendedProperties']['blob_container']
    blob_upload_path = json_activity['typeProperties']['extendedProperties']['blob_upload_path']
    f_type = json_activity['typeProperties']['extendedProperties']['file_type']
    f_prefix = get_key_or_default_from_dict(json_activity['typeProperties']['extendedProperties'],
                                            'output_file_name_prefix',
                                            default='gmail_')
    preceding_str = json_activity['typeProperties']['extendedProperties']['preceding_str']

    # 2b. Fetch emails (Gmails) that meet the criteria based on the 'query'
    token_file_with_path = file_and_sys_utils.get_full_path('usprogrammatic_token.pickle')
    cred_file_with_path = file_and_sys_utils.get_full_path('usprogrammatic_credentials.json')
    service = gmail_utils.get_service(token_file_with_path, cred_file_with_path)
    user_id = 'me'
    q = json_activity['typeProperties']['extendedProperties']['query']
    msg_list = gmail_utils.list_message_with_matching_query(service,
                                                            user_id,
                                                            query=q)
    for m in msg_list:
        # 3a. For each email, scan the msg body for URL with preceding string (optional)
        # Note: get_mime_message function does not parse URLs correctly, and
        # thus is not used in this script
        # mime_msg = get_mime_message(service, 'me', m.get('id'))
        # msg_body = get_mime_msg_body_str(mime_msg)
        msg_id = m.get('id')
        full_msg = gmail_utils.get_full_message(service, 'me', msg_id)
        msg_body = gmail_utils.get_full_message_body_str(full_msg)
        report_url = clean_ttd_report_url(find_ttd_report_url(preceding_str, msg_body)[0])
        # 3b. Once report URL is detected, download it to local data dir
        resp = requests.get(report_url)
        local_file_name = ''.join([f_prefix, datetime.today().strftime('%Y%m%d_%H%M%S'), f_type])
        output_file = os.path.join(local_data_dir, local_file_name)
        with open(output_file, 'wb') as f:
            f.write(resp.content)

        # 3c. Mark the email as read (by removing 'UNREAD' label)
        gmail_utils.mark_as_read(service, user_id, msg_id)

        # 3d. Move the downloaded local data file to Blob
        dest_blob_path_and_name = file_and_sys_utils.join_path_and_file_name(blob_upload_path,
                                                                             local_file_name,
                                                                             separator='/')
        azure_utils.upload_from_local_to_blob(blob_container, output_file, dest_blob_path_and_name)

    print("\nSuccessfully downloaded TTD data from the URL within the email")

    # 4. delete local files (including credentials) and the code folder downloaded temporarily from Azure
    try:
        print("\nThis is current working directory:",file_and_sys_utils.get_full_path(''))
        for extension in ['credentials.json', '.pickle', '.py']:
            files = file_and_sys_utils.list_files_ending_with(file_and_sys_utils.get_full_path(''), extension)
            print("\n=>", files)
            for f in files:
                os.remove(f)
                print("Deleted:", f)

        shutil.rmtree(local_data_dir)
        print("\nDeleted local data folder and its contents:", local_data_dir)
    except OSError as e:
        print("\nError: %s - %s." % (e.filename, e.strerror))


if __name__ == '__main__':
    main()
