"""
Last Modified: May 16, 2019
Author: Phyo Thiha
Description:
Script to send email (via Gmail) in Azure Data Factory.
"""

import json

import usprogrammatic_gmail_account_info
import file_and_sys_utils
import gmail_utils


def main():
    """
    # JSON below is only for testing on your laptop; on production environment, we'll use step 2a. instead
    json_activity = {
        'typeProperties':
            {
                'extendedProperties':
                    {
                        'recipient_emails': 'colgateprogrammatic@gmail.com',
                        'from_email': 'colgateprogrammatic@gmail.com', # required
                        'msg_subject': 'Success msg subject', # required
                        'msg_content': 'Success msg content or body', # required
                    }
            }
    }
    """

    # 1. get 'Extended Properties' passed from Azure Data Factory task
    read_activity = open('activity.json').read()
    json_activity = json.loads(read_activity)
    #"""
    recipient_emails = json_activity['typeProperties']['extendedProperties']['recipient_emails']
    from_email = json_activity['typeProperties']['extendedProperties']['from_email']

    # 2. Send emails
    token_file_with_path = file_and_sys_utils.get_full_path(usprogrammatic_gmail_account_info.TOKEN_FILE)
    cred_file_with_path = file_and_sys_utils.get_full_path(usprogrammatic_gmail_account_info.CREDENTIAL_FILE)
    service = gmail_utils.get_service(token_file_with_path, cred_file_with_path)
    user_id = 'me'
    msg_subject = json_activity['typeProperties']['extendedProperties']['msg_subject']
    msg_content = json_activity['typeProperties']['extendedProperties']['msg_content']
    gmail_utils.send_messsage(service, user_id, from_email, recipient_emails, msg_subject, msg_content)


if __name__ == '__main__':
    main()