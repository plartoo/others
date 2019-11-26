import pdb

import json
import os
import pprint
import requests
from urllib.parse import urljoin, urlparse, urlsplit, quote, unquote, urlencode

import pandas as pd
from twilio.rest import Client


CONFIG_FILE_NAME = 'config.json'
PHONE_DATA_FILE = 'residents_with_valid_numbers_20191123.xlsx'

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


if __name__ == '__main__':
    config = load_config()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(config)

    # message_body = "(cont. from Woodcliff Gardens Event Reminder System) You can ask candidates questions via this online form (please fill out before noon of Nov 12): https://forms.gle/cU8AJCukXWbPsiqy6. We also suggest you to take this pre-election survey as well https://forms.gle/MbiGMTSPgyAv44Sn8 to let the (current and future) board know about your priorities."
    message_body = "From Woodcliff Gardens Event Reminder System => Don't forget to vote for Annual Board Election on TOMORROW at 7PM, Henry Hudson room (8700 basement)!"
    client = Client(config['acnt_sid'], config['auth_token'])

    df = pd.read_excel(PHONE_DATA_FILE)
    # df = pd.read_csv(PHONE_DATA_FILE)
    # message = client.messages.create(
    #     # from_=config['from_num'],
    #     messaging_service_sid=config['messaging_service_sid'],
    #     to='7188011463',
    #     body=message_body,
    # )
    # for to_num in [config['test_to_num'], '540-630-2250', '5406302250']:
    for index, row in df.iterrows():
        # pdb.set_trace()
        to_num = row['CellOrHomePhoneValues']
        if not (pd.isna(to_num) or to_num == 0):
            # print(index,str(to_num))
            message = client.messages.create(
                # from_=config['from_num'],
                messaging_service_sid=config['messaging_service_sid'],
                to=str(to_num),
                body=message_body,
            )
            print(index, '.', to_num, ':', message.sid)

