import pdb

from facebook_business import adobjects
from facebook_business import FacebookSession
from facebook_business import FacebookAdsApi
from facebook_business.adobjects.adaccountuser import AdAccountUser
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.adreportrun import AdReportRun

import json
import os
import pprint
import requests


API_VERSION = 'v4.0'
ACCESS_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token?client_id={app_id}&client_secret={app_secret}&grant_type=client_credentials'
LL_ACCESS_TOKEN_URL = 'https://graph.facebook.com/{api_version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={access_token}'


def get_app_access_token(app_id: str, app_secret: str) -> str:
    url = ACCESS_TOKEN_URL.format(app_id=app_id, app_secret=app_secret)
    resp = requests.get(url)
    data = resp.json()
    return data['access_token']


def get_long_lived_access_token(api_version: str, app_id: str, app_secret: str, user_access_token: str) -> str:
    # Refresh or get long-lived access token
    url = LL_ACCESS_TOKEN_URL.format(api_version=api_version,
                                     app_id=app_id,
                                     app_secret=app_secret,
                                     access_token=user_access_token)
    resp = requests.get(url)
    data = resp.json()
    return data['access_token']


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    this_dir = os.path.dirname(__file__)
    config_filename = os.path.join(this_dir, 'config.json')
    config_file = open(config_filename)
    config = json.load(config_file)
    # app_access_token = get_app_access_token(config['app_id'], config['app_secret'])
    # pdb.set_trace()
    # cur_ll_access_token = config['access_token']
    config_file.close()
    # new_ll_access_token = get_long_lived_access_token(API_VERSION, config['app_id'], config['app_secret'], cur_ll_access_token)
    # config['access_token'] = new_ll_access_token

    # ### Write the new long-lived access token back to config file
    # with open(config_filename, 'w') as outfile:
    #     json.dump(config, outfile)

    ### Setup session and api objects
    session = FacebookSession(
        config['app_id'],
        config['app_secret'],
        config['access_token'],
    )
    api = FacebookAdsApi(session)

    # app_access_token = get_app_access_token(config['app_id'], config['app_secret'])
    # https://developers.facebook.com/docs/facebook-login/access-tokens/#portabletokens
    # Q: where/how do I get user access token (maybe with login dialog prompt) without having to generate one manually first time
    # Or is the flow like this: I download tokens manually once to get a long-lived access token, and then keep refreshing that long-lived access token
    # Q: how do I make sure the access tokens and permissions are right for downloading data in an unrestricted way from all our accounts (asks me to verify my business account etc.)
    # marketing api limits
    # Q: what is/are the best practices to keep the data retrieval rate reasonable/polite and retry
    #
    # Q: Do we need to iterate through campaigns, adsets and ads or would campaigns.get_insights(fields={'level':'ads'}) be sufficient and more efficient?
    # Q: If I set ‘time_increment=1’ in parameters, will it be equivalent to me checking ‘Day’ box in Ads reporting web UI (please see ‘screenshot_1’ attached)?
    # Q: How can I limit the results for ads which are only from campaigns that are delivered/completed? I don’t think ‘delivery_info’ field is supported in API v 4.0.
    # Q: What are the equivalent field names for the following metrics and breakdowns seen in web UI in the API:
    # [https://developers.facebook.com/docs/marketing-api/insights/parameters/v4.0#Fields]
    # ‘Platform’ (publisher_platform?), ‘Placement’ ('platform_position' or 'place_page_id'?),
    # ‘Campaign Budget’, ‘Bid’,
    # ‘Delivery’, ‘Ad Delivery’, ‘Ad Set Delivery’, ‘Campaign Delivery’
    # ‘Results’ ,‘Cost per Result’
    # ‘Unique 2-Second Continuous Video Views’, ‘2-Second Continuous Video Views’, ‘Cost per 2-Second Continuous Video View’
    # ‘3-Second Video Views’, ‘Cost per 3-Second Video View’
    # ‘Unique 10-Second Video Views’, ‘10-Second Video Views’, ‘Cost per-10 Second Video View’
    #
    # Q: what is 'frequency_value' in breakdowns? [https://developers.facebook.com/docs/marketing-api/insights/breakdowns]
    #
    # Q: Is there more up-to-date documentation for Python SDK and API in general with examples?

    FacebookAdsApi.set_default_api(api)
    me = AdAccountUser(fbid='me')#(fbid='100040589411639')#(fbid='114975229923225')#'me')
    # pp.pprint(me.remote_read(fields=[AdUser.Field.name]))
    # pdb.set_trace()
    # my_account = me.get_ad_account()
    accnts = []
    for accnt in me.get_ad_accounts():
        accnts.append(accnt)

    pdb.set_trace()
    print("hello")


    # my_app_id = config['app_id']
    # my_app_secret = config['app_secret']
    # my_access_token = config['access_token']
    # FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
    # pdb.set_trace()
    # my_account = AdAccount('act_1302730239901454') #675301196287656')
    # campaigns = my_account.get_campaigns()
    # print(campaigns)
