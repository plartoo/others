import pdb

import json
import os
import pprint
import requests
from urllib.parse import urljoin, urlparse, urlsplit, quote, unquote, urlencode

CONFIG_FILE_NAME = 'config.json'
BASE_URL = 'https://graph.facebook.com/v4.0/'


def load_config():
    # We can extend this method to allow params, but for now, this is sufficient
    this_dir = os.path.dirname(__file__)
    config_file = open(os.path.join(this_dir, CONFIG_FILE_NAME))
    config = json.load(config_file)
    config_file.close()
    return config


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    config = load_config()
    pp.pprint(config)

    url = urljoin(BASE_URL,'me')
    req = requests.models.PreparedRequest()
    params = {
            'fields':'id,name, adaccounts',
            'access_token':config['access_token']
        }
    all_accnts = []
    req.prepare_url(url, params)
    resp = requests.get(req.url)
    data = resp.json()
    data = data['adaccounts']

    pp.pprint(data)
    while data['data']:
        all_accnts += data['data']
        if 'next' in data['paging']:
            next_url = data['paging']['next']
        else:
            break
        resp = requests.get(next_url)
        data = resp.json()
        pp.pprint(data)
        # pdb.set_trace()
        # print("middle")


    pdb.set_trace()
    print("Done")
