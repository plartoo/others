import pdb

from functools import reduce
import json
import urllib.parse as urlparse
from urllib.parse import urljoin
from urllib.parse import urlencode

import requests

import account_info


PROD_OR_SANDBOX = 'PROD'#'Sandbox'
PRODUCTION_BASE_URL = 'https://api.developer.nielsen.com'
SANDBOX_BASE_URL = 'https://api.sandbox.nielsen.com'
OAUTH_TOKEN_ENDPOINT = 'watch/oauth/token'


def _append_backslash(list_of_paths):
    # append '/' to the end of each of the paths in the list provided
    return list(map(lambda x: ''.join([x,'/']), list_of_paths))


def _url(*url_paths):
    if PROD_OR_SANDBOX == 'Sandbox':
        full_url = _append_backslash([PRODUCTION_BASE_URL] + [i for i in url_paths])
    else:
        full_url = _append_backslash([SANDBOX_BASE_URL] + [i for i in url_paths])
    # Note: we need to strip the last '/' because Nielsen API wouldn't work with that
    return reduce(urljoin, full_url).strip('/')


def add_request_body(url, req_body):
    # REF: https://stackoverflow.com/a/2506477/1330974
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(req_body)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def get_token():
    request_body = {
        'grant_type': 'password',
        'username': account_info.USERNAME,
        'password': account_info.PWD
    }
    request_headers = {
        'Authorization': ''.join(['Basic ', account_info.SECRET_KEY]),
        'Content-Type': 'application/x-www-form-urlencoded;charset="UTF-8"'
    }
    url = _url(OAUTH_TOKEN_ENDPOINT)
    print(url)
    print(request_body)
    print(request_headers)
    # rsp = requests.post(url, params=json.dumps(request_body), headers=request_headers)
    rsp = requests.post(url, headers=request_headers, data=request_body)
    print(rsp.text)
    print('haha')
get_token()
