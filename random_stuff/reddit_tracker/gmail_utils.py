"""
Description: 
A small Python module to send gmail through an authenticated 
account using Gmail API. See below link for official guide:
https://developers.google.com/gmail/api/quickstart/python

Note: Only the essential methods from my other gmail_utils.py
module is imported here. I also updated the comments
and modified the code a little here because the
last time I wrote gmail_utils.py for other projects was
more than a year ago.
"""
import base64
import json
import os.path
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def get_service(token_file_with_path, cred_file_with_path):
    """
    First call you must make before doing anything with Gmail API.
    Before calling this function, you must create and download
    credentials.json file from Google Cloud Console as detailed
    in this URL:
    https://developers.google.com/workspace/guides/create-credentials

    After credentials.json file is downloaded from the Google Cloud
    Console, you can invoke this function. Calling this function will
    begin an authentication flow for Gmail API and generate a token
    JSON file, if none exists already, in the same folder as this file.
    That token JSON file will be used to create service objects in
    the future calls.

    If token and credential files already exist, you can pass
    their paths as parameter to this call.

    Returns the gmail service built from token and credential
    files.
    """
    credentials = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    return build('gmail', 'v1', credentials=credentials)


def create_message(sender_email, to_email, subject, message_text):
    """
    REF: https://developers.google.com/gmail/api/guides/sending#python
    Create a message for an email.

    Args:
        sender_email: Email address of the sender.

        to_email: Email address of the receiver.
        If sending to multiple emails, join them in
        a string with ';' as delimiter. E.g.,
        'email1@gmail.com;email2@gmail.com'.

        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
  """
    message = MIMEText(message_text, 'html')
    message['to'] = to_email
    message['from'] = sender_email
    message['subject'] = subject

    return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}


def send_message(service, user_id, message):
    """
    REF: https://developers.google.com/gmail/api/guides/sending#python
    Send an a gmail message. Before calling this method, we must
    prepare a message using 'create_message' method.

    Args:
        service: Authorized Gmail API service instance.

        user_id: Sender's email address. If you are sending using
        credentials.json and token.json files (that is, from your
        authenticated gmail account), you can just enter "me" for
        this input parameter.

        message: Message to be sent. This message object should be
        created by create_message function above.

    Returns:
        Sent message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Sent gmail with message id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)

