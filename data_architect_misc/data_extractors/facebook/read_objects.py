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
        'level': 'ads',
        'filtering': [{'date_preset': 'last_week_mon_sun'}],#[{'field': 'delivery_info', 'operator': 'IN', 'value': ['completed', 'recently_completed']}],
        'breakdowns': ['days_1', 'age', 'gender', 'ad_id'],
        'time_range': {'since': '2019-10-10', 'until': '2019-10-17'},
    }


    FacebookAdsApi.set_default_api(api)

    print('\n\n\n********** Reading objects example. **********\n')

    ### Setup user and read the object from the server
    me = AdUser(fbid='me')

    ### Read user permissions
    print('>>> Reading permissions field of user:')
    pp.pprint(me.remote_read(fields=[AdUser.Field.name]))

    ### Get first account connected to the user
    my_account = me.get_ad_account()

    # https://developers.facebook.com/docs/marketing-api/insights/parameters/v4.0
    # level
    # account > Campaign > Ad Set (adset) > Ad
    # ***Day (time_increment==1?)
    # Breakdowns
    #   age, gender,
    #   country,
    #   ***impression_device, platform (publisher_platform?), device_platform, [NO 'placement', but maybe it's 'platform_position' or 'place_page_id'?]
    #   *** what is 'frequency_value' in breakdowns?
    #   Dynamic Creative Asset
    #       call_to_action_asset (Call To Action)
    #       description_asset (Description)
    #       link_url_asset (Website URL)
    #       product_id (Product)
    #
    # action_breakdowns
    #   None (= default value of 'action_type')
    #   action_device (Conversion Device?)
    #   action_carousel_card_id, action_carousel_card_name (Carousel)
    #   action_destination (Destination)
    #   action_video_sound (VideoSound)
    #   action_video_type (VideoViewType)
    # date_preset
    #   last_week_mon_sun
    #
    # https://developers.facebook.com/docs/marketing-api/insights/parameters/v4.0#Fields
    # date_start (reporting starts)
    # date_stop (reporting ends)
    # account_currency (Currency)
    # objective
    # campaign_id
    # campaign_name
    # account_id
    # account_name
    # adset_id
    # adset_name
    # ad_id
    # ad_name

    # impressions
    # frequency (The average number of times each person saw your ad. estimated)
    # reach
    # clicks
    # spend (Amount Spent; The estimated total amount of money you've spent on your campaign, ad set or ad during its schedule)
    # conversions ( total number of conversions attributed to your ads, including contact, customize_product, donate, find_location, schedule, start_trial, submit_application, subscribe)
    # conversion_values (total value of all conversions attributed to your ads, including contact, customize_product, donate, find_location, schedule, start_trial, submit_application, subscribe)
    # cost_per_action_type
    # cost_per_conversion
    # cost_per_estimated_ad_recallers (Cost per Estimated Ad Recall Lift)
    #
    # cpc (cost per click)
    # cpm (cost per milli)
    # cpp (Cost per 1,000 People Reached)
    # ctr (percentage of times people saw your ad and performed a click (all))
    # estimated_ad_recallers (An estimate of the number of additional people who may remember seeing your ads, if asked, within 2 days. This metric is only available for assets in the Brand awareness, Post engagement and Video views Objectives)
    # estimated_ad_recall_rate (The rate at which an estimated number of additional people, when asked, would remember seeing your ads within 2 days. This metric is only available for assets in the Brand awareness, Post engagement and Video views Objectives)
    # video_30_sec_watched_actions (The number of times your video played for at least 30 seconds, or for nearly its total length if it's shorter than 30 seconds. For each impression of a video, we'll count video views separately and exclude any time spent replaying the video.)
    # video_avg_time_watched_actions (The average time a video was played, **including any time spent replaying the video for a single impression**)
    # video_p100_watched_actions (number of times video was fully played including the skip-to-the-end views)
    # video_p25_watched_actions
    # video_p50_watched_actions
    # video_p75_watched_actions
    # video_p95_watched_actions
    # video_thruplay_watched_actions (ThruPlays; either fullly played or for at least 15 seconds)
    # cost_per_thruplay (Cost per ThruPlay)


    # **buying_type (only visible at campaign level; The method by which you pay for and target ads in your campaigns: through dynamic auction bidding, fixed-price bidding, or reach and frequency buying)

    # actions (total number of actions people took that are attributed to your ads. Actions may include engagement, clicks or conversions)
    # unique_actions (The number of people who took an action that was attributed to your ads. This metric is estimated)
    # action_values (total value of all conversions attributed to your ads)
    # unique_clicks (The number of people who performed a click (all). This metric is estimated.)
    # unique_ctr
    # unique_outbound_clicks
    # unique_outbound_clicks_ctr
    # unique_inline_link_clicks
    # unique_inline_link_click_ctr
    # cost_per_inline_link_click
    # cost_per_inline_post_engagement
    # cost_per_outbound_click
    # cost_per_unique_outbound_click (estimated)
    # cost_per_unique_action_type (estimated)
    # cost_per_unique_click (estimated)
    # full_view_reach (The number of people who performed a Full View on your Page's post as a result of your ad. Reach is different from impressions, which may include multiple views of your ads by the same people.)
    # full_view_impressions (The number of Full Views on your Page's posts as a result of your ad.)
    # outbound_clicks (The number of clicks on links that take people off Facebook-owned properties)
    # outbound_clicks_ctr (The percentage of times people saw your ad and performed an outbound click.)
    # purchase_roas (The total return on ad spend (ROAS) from purchases. This is based on information received from one or more of your connected Facebook Business Tools and attributed to your ads.)
    # **quality_ranking (only available on ad level; A ranking of your ad's perceived quality. Quality is measured using feedback on your ads and the post-click experience. Your ad is ranked against ads that competed for the same audience. Possible values include BELOW_AVERAGE_10, BELOW_AVERAGE_20, BELOW_AVERAGE_35, AVERAGE, ABOVE_AVERAGE, or UNKNOWN if there's not enough information about the ad. This metric is an ad relevance diagnostic (https://www.facebook.com/help/403110480493160))
    # video_play_actions (Video Plays; number of times videos starts playing; excludes replays. metrics in development)
    # website_ctr (The percentage of times people saw your ad and performed a link click)


    #               ***Bid, Campaign Budget
    # Performance: 	***Delivery, Ad Delivery, Ad Set Delivery, Campaign Delivery (The current status of your campaign, ad set or ad delivery)
    #               ***Results, Cost per Result,
    #
    # Impressions
    # Frequency
    # Reach
    # Clicks (All),
    # Amount Spent,
    # CPM,
    # Cost per 1,000 People Reached
    #
    # Engagement: 	***Unique 2-Second Continuous Video Views, 2-Second Continuous Video Views, Cost per 2-Second Continuous Video View,
    # 				*** 3-Second Video Views, Cost per 3-Second Video View,
    #               *** 10-Second Video Views, Cost per-10 Second Video View, Unique 10-Second Video Views,
    #
    # **Video Average Watch Time (video_avg_time_watched_actions)
    #
    # Video Plays (video_play_actions)
    # ThruPlays (video_thruplay_watched_actions)
    # Cost per ThruPlay,
    # CTR (Link Click-Through Rate),
    # Estimated Ad Recall Lift,
    # Estimated Ad Recall Lift Rate,
    # Cost per Estimated Ad Recall Lift

    accnt = [a for a in me.get_ad_accounts() if a['account_id'] == '609465202905776'][0]
    accnt.get_ads()[0]
    # get_insights(fields=fields,params=params,))
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
