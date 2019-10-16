# Copyright 2014 Facebook, Inc.

# You are hereby granted a non-exclusive, worldwide, royalty-free license to
# use, copy, modify, and distribute this software in source code or binary
# form for use in connection with the web services and APIs provided by
# Facebook.

# As with any software that integrates with the Facebook platform, your use
# of this software is subject to the Facebook Developer Principles and
# Policies [http://developers.facebook.com/policy/]. This copyright notice
# shall be included in all copies or substantial portions of the software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from facebookads.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.api import FacebookAdsApi
from facebookads.adobjects.adsinsights import AdsInsights
# from facebookads.api import FacebookAdsApi

access_token = ''
ad_account_id = ''
app_secret = ''
app_id = ''
FacebookAdsApi.init(access_token=access_token)

fields = [
    'results',
    'reach',
    'frequency',
    'impressions',
    'delivery',
    'spend',
    'cost_per_result',
    'cpp',
    'cpm',
    'actions:like',
    'actions:comment',
    'actions:post_reaction',
    'actions:onsite_conversion_post_save',
    'actions:post',
    'actions:full_view',
    'unique_actions:full_view',
    'cost_per_action_type:post_engagement',
    'cost_per_action_type:like',
    'cost_per_action_type:page_engagement',
    'campaign_group_name',
    'campaign_group_id',
    'campaign_name',
    'campaign_id',
    'adgroup_id',
    'adgroup_name',
    'account_id',
    'account_name',
    'date_start',
    'date_stop',
    'bid',
    'buying_type',
    'objective',
    'schedule',
    'budget',
    'cost_per_action_type:link_click',
    'cpc',
    'unique_video_continuous_2_sec_watched_actions:video_view',
    'video_continuous_2_sec_watched_actions:video_view',
    'cost_per_2_sec_continuous_video_view:video_view',
    'cost_per_action_type:video_view',
    'video_10_sec_watched_actions:video_view',
    'unique_video_view_10_sec:video_view',
    'cost_per_10_sec_video_view:video_view',
    'video_p100_watched_actions:video_view',
    'actions:video_view',
    'video_thruplay_watched_actions:video_view',
    'cost_per_thruplay:video_view',
    'unique_link_clicks_ctr',
    'video_avg_time_watched_actions:video_view',
    'video_play_actions:video_view',
    'website_ctr:link_click',
    'estimated_ad_recallers',
    'estimated_ad_recall_rate',
    'cost_per_estimated_ad_recallers',
    'clicks',
    'unique_clicks',
    'ctr',
    'unique_ctr',
    'actions:photo_view',
]
params = {
    'level': 'ad',
    'filtering': [{'field':'delivery_info','operator':'IN','value':['completed','recently_completed']}],
    'breakdowns': ['days_1','age','gender','ad_id'],
    'time_range': {'since':'2019-10-10','until':'2019-10-17'},
}
print(AdAccount(ad_account_id).get_insights(
    fields=fields,
    params=params,
))


