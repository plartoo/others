import pdb

import pickle
import os.path
from pprint import pprint

from googleapiclient import discovery
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCRIPT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# REF: https://developers.google.com/sheets/api/guides/authorizing
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1aFkTIdJZy8e-yUm2dbQ1pqsl84Mpi0kUdcmHYSm-gMw'
SPREADSHEET_SHEET_1_NAME = 'Emails'
SPREADSHEET_SHEET_1_RANGE = 'A:A'
SPREADSHEET_SHEET_2_NAME = 'Pwd'
SPREADSHEET_SHEET_1_RANGE = 'A:A'


def get_range_str(sheet_name, sheet_range):
    # REF: https://developers.google.com/sheets/api/guides/concepts
    return '!'.join([sheet_name, sheet_range])


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print('no creds')
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(SCRIPT_DIR_PATH, 'config','credentials.json'),
                SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    # REF1: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
    # REF2: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=get_range_str(SPREADSHEET_SHEET_1_NAME,
                                                    SPREADSHEET_SHEET_1_RANGE),
                                # majorDimension = 'COLUMNS'
                                ).execute()

    values = result.get('values', [])

    if not values:
        print('No data.')
    else:
        pdb.set_trace()
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s' % (row[0]))

if __name__ == '__main__':
    main()