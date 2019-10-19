import pdb

from facebook_business import FacebookSession
from facebook_business import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign as AdCampaign
from facebook_business.adobjects.adaccountuser import AdAccountUser as AdUser

import json
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)
this_dir = os.path.dirname(__file__)
config_filename = os.path.join(this_dir, 'config.json')

config_file = open(config_filename)
config = json.load(config_file)
config_file.close()

### Setup session and api objects
session = FacebookSession(
    config['app_id'],
    config['app_secret'],
    config['access_token'],
)
api = FacebookAdsApi(session)


if __name__ == '__main__':
    FacebookAdsApi.set_default_api(api)

    print('\n\n\n********** Reading objects example. **********\n')

    ### Setup user and read the object from the server
    me = AdUser(fbid='me')

    ### Read user permissions
    print('>>> Reading permissions field of user:')
    pp.pprint(me.remote_read(fields=[AdUser.Field.name]))

    ### Get first account connected to the user
    my_account = me.get_ad_account()

    accnt = [a for a in me.get_ad_accounts() if a['account_id'] == '609465202905776'][0]
    accnt.get_ad_sets()[0]
    pdb.set_trace()

    # ### Read connections (in this case, the accounts connected to me)
    # # Pro tip: Use list(me.get_ad_accounts()) to make a list out of
    # # all the elements out of the iterator
    # my_accounts_iterator = me.get_ad_accounts()
    # i = 0
    # print('>>> Reading accounts associated with user')
    # for account in my_accounts_iterator:
    #     i += 1
    #     print(i)
    #     pp.pprint(account)


    print(">>> Campaign Stats")
    for campaign in my_account.get_campaigns(fields=[AdCampaign.Field.name]):
        for stat in campaign.get_stats(fields=[
            'impressions',
            'clicks',
            'spent',
            'unique_clicks',
            'actions',
        ]):
            print(campaign[campaign.Field.name])
            for statfield in stat:
                print("\t%s:\t\t%s" % (statfield, stat[statfield]))

#https://github.com/facebook/facebook-python-business-sdk/blob/master/facebook_business/adobjects/adaccount.py
#get_ads(self, fields=None, params=None, batch=None, success=None, failure=None, pending=False)
#get_ad_sets(self, fields=None, params=None, batch=None, success=None, failure=None, pending=False)
