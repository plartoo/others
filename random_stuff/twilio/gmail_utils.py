import base64
import email
import os.path
import pickle

from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']#['https://www.googleapis.com/auth/gmail.modify']


def create_message(sender, to, subject, message_text):
  """
  REF: https://developers.google.com/gmail/api/v1/reference/users/messages/send
  Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}


def send_message(service, user_id, message):
  """
  REF: https://developers.google.com/gmail/api/v1/reference/users/messages/send
  Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def get_service(token_file_with_path, cred_file_with_path):
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file_with_path):
        with open(token_file_with_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file_with_path,
                                                             SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open(token_file_with_path, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def list_message_with_matching_query(service, user_id, query=''):
    """
    REF: https://developers.google.com/gmail/api/v1/reference/users/messages/list
    List all Messages of the user's mailbox matching the query.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg 1.- 'from:user@some_domain.com' for Messages from a particular sender.
        Eg 2. - 'in:inbox is:unread subject:TOM Basic newer_than:1d' for unread
        messages in inbox from less than 1 day ago with subject that includes 'Tom Basic'
        For more about queries: https://support.google.com/mail/answer/7190?hl=en

    Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   q=query).execute()
        messages = []

        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:
        print("An error occurred:\n", error)


def list_message_with_label(service, user_id, label_ids=[]):
    """
    REF: https://developers.google.com/gmail/api/v1/reference/users/messages/list
    List all Messages of the user's mailbox with label_ids applied.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.

    Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                                                       labelIds=label_ids,
                                                       pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError as error:
        print("An error occurred:\n", error)


def get_full_message(service, user_id, msg_id):
    """
    Get a Message with given ID.
    REF: https://developers.google.com/gmail/api/v1/reference/users/messages/get

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

    Returns:
        A Message.
    """
    try:
        message = service.users().messages().get(userId=user_id,
                                                 id=msg_id,
                                                 format='full').execute()
        return message
    except errors.HttpError as error:
        print("An error occurred:\n", error)


def get_full_message_body_str(full_msg):
    return str(base64.urlsafe_b64decode(full_msg.get('payload').get('parts')[0].get('body').get('data')))


def get_full_message_body_HTML(full_msg):
    return str(base64.urlsafe_b64decode(full_msg.get('payload').get('parts')[1].get('body').get('data')))


def get_mime_message(service, user_id, msg_id):
    """
    Get a Message and use it to create a MIME Message.
    REF: https://developers.google.com/gmail/api/v1/reference/users/messages/get

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

    Returns:
        A MIME Message, consisting of data from Message.
    """
    try:
        message = service.users().messages().get(userId=user_id,
                                                 id=msg_id,
                                                 format='raw').execute()
        # Note: in certain emails, the URL is decoded (incorrectly) with new line characters
        msg_bytes = base64.urlsafe_b64decode(message['raw'])
        mime_msg = email.message_from_bytes(msg_bytes)
        return mime_msg
    except errors.HttpError as error:
        print("An error occurred:\n", error)


def get_mime_msg_body_str(mime_msg):
    body = ''
    if mime_msg.is_multipart():
        # we'll just concat the body of messages in the entire thread
        for payload in mime_msg.get_payload():
            body = ''.join([body, payload.get_payload()])
    else:
        body = ''.join([body, mime_msg.get_payload()])
    return body


def modify_message(service, user_id, msg_id, msg_labels):
    """
    Modify the Labels on the given Message.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
        msg_id: The id of the message required.
        msg_labels: The change in labels.

    Returns:
        Modified message, containing updated labelIds, id and threadId.
    """
    try:
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                                                    body=msg_labels).execute()
        label_ids = message['labelIds']
        print('Message ID: %s - now with Label IDs %s' % (msg_id, label_ids))
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


def remove_unread_message_label():
    """
    Create object to update labels.
    REF: https://developers.google.com/gmail/api/guides/labels

    Returns:
        A label update object.
    """
    return {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}


def mark_as_read(service, user_id, msg_id):
    """
    Mark the message as 'READ' (by removing 'UNREAD' label).
    """
    modify_message(service, user_id, msg_id, remove_unread_message_label())


def trash_message(service, user_id, msg_id):
    """
    Send the message to Trash.
    REF: https://developers.google.com/gmail/api/v1/reference/users/messages/trash
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
                can be used to indicate the authenticated user.
        msg_id: The id of the message required.
    """
    try:
        service.users().messages().trash(userId=user_id, id=msg_id).execute()
        print('Message ID: %s - is deleted' % msg_id)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
