import pdb

import json
import os
import pprint
import requests
from urllib.parse import urljoin, urlparse, urlsplit, quote, unquote, urlencode

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say


CONFIG_FILE_NAME = 'config.json'


def load_config():
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

    message_body = "Testing sms"

    client = Client(config['acnt_sid'], config['auth_token'])
    # https://www.twilio.com/docs/voice/twiml/say
    response = VoiceResponse()
    response.say('How are you fatty?', voice='woman', loop=1)
    print(response)

    call = client.calls.create(
        # url='http://demo.twilio.com/docs/voice.xml',
        from_=config['from_num'],
        to=config['test_to_num'],
        # url='https://www.dropbox.com/s/jhg56frh3enge7y/hello.xml?dl=0'#'http://127.0.0.1:5000/record'
        # url='http://0.0.0.0:8000/voice.xml',
    )

    print(call.sid)
