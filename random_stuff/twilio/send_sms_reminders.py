import pdb

import json
import os
import pprint
import re
import requests
from urllib.parse import urljoin, urlparse, urlsplit, quote, unquote, urlencode

import pandas as pd
from twilio.rest import Client


CONFIG_FILE_NAME = 'config.json'
# this file was used before Jan 27, 2020 text message and it has all residents' numbers 'residents_with_valid_numbers_20191123.xlsx'
PHONE_DATA_FILE = 'WoodcliffResidentCellandEmailAddressCollectionForReminderSystem_20200126.xlsx'

def load_config():
    # config.json file should be like this:
    # {
    #     "acnt_sid": "",
    #     "auth_token": "",
    #     "messaging_service_sid": "",
    #     "from_num": "+12018000000",
    #     "test_to_num": "+17188000000"
    # }
    # We can extend this method to allow params, but for now, this is sufficient
    this_dir = os.path.dirname(__file__)
    config_file = open(os.path.join(this_dir, CONFIG_FILE_NAME))
    config = json.load(config_file)
    config_file.close()
    return config


def convert_from_array_to_dict(lst):
    i = iter(lst)
    return dict(zip(i, i))


if __name__ == '__main__':
    config = load_config()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(config)

    # Step 1: Update the message first.
    # message_body = "(cont. from Woodcliff Gardens Event Reminder System) You can ask candidates questions via this online form (please fill out before noon of Nov 12): https://forms.gle/cU8AJCukXWbPsiqy6. We also suggest you to take this pre-election survey as well https://forms.gle/MbiGMTSPgyAv44Sn8 to let the (current and future) board know about your priorities."
    # message_body = "From Woodcliff Gardens Event Reminder System => Please check out the board election results and other update/surveys on our community website: http://woodcliffgardens.net"
    message_body = "From Woodcliff Gardens Event Reminder System => We have shareholders meeting tomorrow (Tuesday, January 28, 2020 - 7:30PM) at Henry Hudson room (basement of #8700)."
    # message_body = "You can always reply 'STOP' to stop receiving messages from this system and text 'START' to resume receiving messages."
    client = Client(config['acnt_sid'], config['auth_token'])

    col_name = "Your Cell Phone (Optional. If you don't want to receive texts, please leave this blank and we will only send you email reminders using the email address you've provided above.)"
    df = pd.read_excel(PHONE_DATA_FILE, dtype={col_name: str})
    # df = pd.read_csv(PHONE_DATA_FILE, dtype={'CellOrHomePhoneValues': str})


    # # Step 2: Try this first to see how the message looks on ** my number ** (enter below)
    # message = client.messages.create(
    #     # from_=config['from_num'],
    #     messaging_service_sid=config['messaging_service_sid'],
    #     to='',
    #     body=message_body,
    # )

    # Step 3: Uncomment below and run it when both message and the numbers are good.
    num_arr = []
    for index, row in df.iterrows():
        to_num = row[col_name]
        if not (pd.isna(to_num) or str(to_num) == '0'):
            to_num = re.sub(r'\D', '', to_num)  # strip everything except digits
            num_arr.append(to_num)

    # Make sure we only send one message per phone number
    num_dict = dict.fromkeys(num_arr,1)

    i = 0
    for to_num, const in num_dict.items():
        i += 1
        print(i, '=>', to_num)
        message = client.messages.create(
            # from_=config['from_num'],
            messaging_service_sid=config['messaging_service_sid'],
            to=str(to_num),
            body=message_body,
        )
        print(message.sid)

