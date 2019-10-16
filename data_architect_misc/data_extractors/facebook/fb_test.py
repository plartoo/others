import pdb

import facebook_business
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount


my_app_id = ''
my_app_secret = ''
my_access_token = ''
me = facebook_business.adobjects.adaccount.AdAccount(fbid='me')

pdb.set_trace()
ad_account_id = ''# 'act_540282000099285'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
# pdb.set_trace()
my_account = AdAccount('{0}'.format(ad_account_id)) #'act_{0}'.format(account_id))
campaigns = my_account.get_campaigns()
print(campaigns)

# https://github.com/facebook/facebook-python-business-sdk/tree/master/examples
# https://github.com/facebook/facebook-python-business-sdk/blob/master/examples/AdsInsightsEdgeAdCampaignInsights.py
# https://github.com/facebook/facebook-python-business-sdk/blob/master/examples/AdsInsightsEdgeStoreVisitsAdCampaignInsights.py
# curl -i -X GET "https://graph.facebook.com/{app_id}?fields=id,name&access_token={}"
#
# Write email to Yanbin to help with these:
# 1. permission
# 2. access token refresh
# 3. linking to other FB accounts
# 4. in 'read_object.py' WARNING:root:`remote_read` is being deprecated, please update your code with new function
# AttributeError: 'AdAccount' object has no attribute 'get_ad_campaigns' etc. Where do I get the lastest Documentation for Python SDK
# 5.
#https://developers.facebook.com/apps/1302730239901454/app-review/submissions/current-request/
# Next to try:
# https://developers.facebook.com/docs/marketing-api/insights

# https://github.com/facebook/facebook-python-business-sdk/blob/master/facebook_business/adobjects/abstractcrudobject.py#L312
#Object(id).api_get() instead

# (Pdb) me.get_ad_account()
# <AdAccount> {
#     "account_id": "1904787169752419",
#     "id": "act_1904787169752419"
# }
# (Pdb) me
# <AdAccountUser> {
#     "id": "140211607341819",
#     "name": "Colgate BM"
# }