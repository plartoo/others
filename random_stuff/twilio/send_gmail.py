import pdb

import base64
import json
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
import pandas as pd


import gmail_utils


def get_full_path(dir_name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), dir_name)


def myprint(j):
    print(json.dumps(j, sort_keys=True, indent=4))


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    TOKEN_FILE = 'woodcliffreminder_token.pickle'
    CREDENTIAL_FILE = 'woodcliffreminder_credentials.json'
    EMAIL_DATA_FILE = 'WoodcliffResidentCellandEmailAddressCollectionForReminderSystem_20200126.xlsx' #'residents_with_valid_numbers_20191123.xlsx'

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_FILE, gmail_utils.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    token_file_with_path = get_full_path(TOKEN_FILE)
    cred_file_with_path = get_full_path(CREDENTIAL_FILE)
    service = gmail_utils.get_service(token_file_with_path, cred_file_with_path)
    user_id = 'me'
    # msg_list = gmail_utils.list_message_with_matching_query(service,
    #                                                         user_id,
    #                                                         query='from:no-reply@accounts.google.com')
    # for m in msg_list:
    #     msg_id = m.get('id')
    #     full_msg = gmail_utils.get_full_message(service, 'me', msg_id)
    #     myprint(full_msg)
    #     print(gmail_utils.get_full_message_body_str(full_msg))

    df = pd.read_excel(EMAIL_DATA_FILE)
    # df = pd.read_csv(EMAIL_DATA_FILE)


    ## Step 1: Update subjct and message_text below.
    subject = 'Woodcliff Gardens Reminder System: Shareholders meeting tomorrow (Tuesday, January 28, 2020 - 7:30PM at #8700 basement)'
    message_text = """
    <br><br>
    Dear Shareholders,
    <br><br>
    We have shareholders (open) meeting tomorrow (Tuesday, January 28, 2020 - 7:30PM) at Henry Hudson room (#8700 basement).</b>
    <br><br>
    You are receiving this email because you have subscribed to Woodcliff reminder system. If you'd like to unsubscribe from this list, please reply this email with message 'unsubscribe' and we'll review it monthly to remove you from it.
    <br><br>
    See you there!
    <br>
    """

    sent_emails = {}
    i = 0
    for index, row in df.iterrows():
        raw_to_email = row['Email Address']
        if not (pd.isna(raw_to_email) or raw_to_email == 'NA'):
            emails = raw_to_email.split(';')
            to_emails = []

            for e in emails:
                if (e in sent_emails) or (e == ''):
                    continue
                else:
                    sent_emails[e] = 1
                    to_emails.append(e)

            to_email = ';'.join(to_emails)

            if to_email:
                ## Step 2: Test sending the message with ** my email ** (enter it here) below first
                # msg = gmail_utils.create_message('woodcliffreminder@gmail.com', '', subject, message_text)
                # gmail_utils.send_message(service, user_id, msg)
                # exit(0)

                ## Step 3: visually inspect all emails first.
                # print(index+1, '=>', str(to_email))

                ## Step 4: After step 2 testing, uncomment this below and send this out to everyone
                msg = gmail_utils.create_message('woodcliffreminder@gmail.com', to_email, subject, message_text)
                print(index+1, '=>', str(to_email))
                gmail_utils.send_message(service, user_id, msg)


if __name__ == '__main__':
    main()
