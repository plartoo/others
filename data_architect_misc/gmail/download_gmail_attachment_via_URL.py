import pdb

import os
import requests
import re
import sys
import uuid

import usprogrammatic_gmail_account_info
import gmail_utils


def get_full_path(dir_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_name)

def append_new_sys_path(dir_name):
    new_sys_path = get_full_path(dir_name)
    if new_sys_path not in sys.path:
        sys.path.append(new_sys_path)
        print("\nNew sys path appended:", new_sys_path)
        print("Current sys path is:\n", sys.path, "\n")


def find_urls(s):
    return re.findall(r'(https?://\S+)',s)


def find_ttd_report_url(s):
    return re.findall(r'clicking the link below.*(https?://\S+)', s, re.S)


def clean_ttd_report_url(url):
    return url.replace('\\r\\n', '')


def main():
    local_dir_base_name = str(uuid.uuid4())
    local_code_dir_name = ''.join(['code_',local_dir_base_name])
    local_data_dir_name = ''.join(['data_',local_dir_base_name])
    append_new_sys_path(local_code_dir_name)
    local_code_dir = get_full_path(local_code_dir_name)

    #"""
    # The JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    json_activity = {
        'typeProperties':
            {
                'extendedProperties':
                    {
                        'blob_container': 'pacing-report',
                        'blob_credential_dir_path': 'code/gmail_url_download/credentials',
                        'blob_helper_code_dir_path': 'code/gmail_url_download/helpers',
                        'blob_main_code_dir_path': 'code/gmail_url_download/main',
                        'query':'',
                    }
            }
    }
    """
    # 2a. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    """

    for k in ['blob_credential_dir_path',]:


    # user_id = 'me'
    # # q = 'in:inbox is:unread subject:Colgate Programmatic Phyo GroupM Redfuse newer_than:1d'
    # q = 'in:inbox subject:Colgate Programmatic Phyo GroupM Redfuse newer_than:1d'
    # msg_list = gmail_utils.list_message_with_matching_query(service,
    #                                                         user_id,
    #                                                         query=q)
    # for m in msg_list:
    #     # Note: get_mime_message function does not parse URLs correctly, and
    #     # thus is not used in this script
    #     # mime_msg = get_mime_message(service, 'me', m.get('id'))
    #     # msg_body = get_mime_msg_body_str(mime_msg)
    #
    #     full_msg = gmail_utils.get_full_message(service, 'me', m.get('id'))
    #     msg_body = gmail_utils.get_full_message_body_str(full_msg)
    #     report_url = clean_ttd_report_url(find_ttd_report_url(msg_body)[0])
    #     resp = requests.get(report_url)
    #     print(resp.status_code)
    #     print(resp.headers['content-type'])
    #     print(resp.encoding)
    #     # with open('test.xlsx', 'wb') as f:
    #     #     f.write(resp.content)
    #
    #     pdb.set_trace()
    #     print("\n")

    # pdb.set_trace()
    print("Done")


if __name__ == '__main__':
    main()