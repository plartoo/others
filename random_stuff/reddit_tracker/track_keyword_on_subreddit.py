"""
Description: Script to track some interested keywords on Reddit using its API.
The script follows the example shown in this URL:
https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example

Usage:
python track_keyword_on_subreddit.py -s <subreddit_name> -k <keyword_to_detect> -m <how_often_to_check_in_minutes>

For example:
>> python track_keyword_on_subreddit.py -s "r/gamesale/new" -l 10 -k "megaman 11" -m 5
The above command will check "Megaman 11" keyword in the 10 most recent posts of the subreddit
"r/gamesale/new" every 5 minutes.

>> python track_keyword_on_subreddit.py -s r/gamesale/new -k "\[H\].*PS4" -m 5
The above command will check the strings that has "[H].*PS4" keyword in
the lastest 100 posts in the subreddit r/gamesale/new every 5 minutes.

>> python track_keyword_on_subreddit.py -s r/gamesale/new
-k "\[H\].*Super Mario" "\[H\].*Mega.*man" -m 5
The above command will track two keywords, namely "\[H\].*Super Mario" and
"\[H\].*Mega.*man", in the subreddit "r/gamesale/new" every 5 minutes.

Other notes:
Before running this script, you have to client_id and client_secret from 
Reddit as explained in the URL below:
https://github.com/reddit-archive/reddit/wiki/OAuth2

As of Apr 26, 2021, Reddit allows 60 requests per minute via OAuth2 as per
the URL below:
https://github.com/reddit-archive/reddit/wiki/API
Please check the API etiquette before using this script (Default is set to
once every five minutes).

Reddit API endpoints:
https://www.reddit.com/dev/api

This article below is a decent intro to Reddit API:
https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c
https://web.archive.org/web/20210426204532/https://towardsdatascience.com/how-to-use-the-reddit-api-in-python-5e05ddfd1e5c?gi=4d6f3ddaf2fd
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta
from urllib.error import HTTPError

import requests
import requests.auth

from reddit_account_info import client_id, client_secret, username, pwd
from track_keyword_on_subreddit_account_info import recipient_emails, sender_email
import gmail_utils


GMAIL_TOKEN_FILE = 'token.json'
GMAIL_CREDENTIAL_FILE = 'credentials.json'

REDDIT_API_URL = 'https://oauth.reddit.com/'
ACCESS_TOKEN_URL = 'https://www.reddit.com/api/v1/access_token'
USER_AGENT = "Subreddit Keyword Checker"


def get_token_expiration_datetime_object(cur_datetime, expires_in_secs):
    return cur_datetime + timedelta(seconds=expires_in_secs)


def generate_new_access_token(client_id,
                              client_secret,
                              username,
                              pwd,
                              current_token=None,
                              current_token_expires_on=None):
    """
    Generates and returns a new access token along with the expiration
    datetime object if the existing one, as indicated by the
    current_token_expires_on parameter, has expired (based on comparison
    with the current datetime).

    If the current_token or the current_token_expires_on parameter is None
    (None is default for both), then the access token is generated and
    returned with a datetime object indicating the expiration datetime
    in the future.
    """
    cur_datetime = datetime.now()

    try:
        if current_token is None:
            # REF: https://github.com/reddit-archive/reddit/wiki/OAuth2#retrieving-the-access-token
            data = {"grant_type": "password",
                    "username": username, "password": pwd}
        else:
            if cur_datetime >= current_token_expires_on:
                # REF: https://github.com/reddit-archive/reddit/wiki/OAuth2#refreshing-the-token
                data = {"grant_type": "refresh_token",
                        "refresh_token": current_token}

            else:
                return current_token, current_token_expires_on

        resp = requests.post(ACCESS_TOKEN_URL,
                             auth=requests.auth.HTTPBasicAuth(client_id, client_secret),
                             data=data,
                             headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        return resp.json()['access_token'], get_token_expiration_datetime_object(cur_datetime,
                                                                                 resp.json()['expires_in'])
    except HTTPError as http_err:
        sys.exit(f"HTTP Error occurred in fetching new access token: {http_err}")
    except Exception as err:
        sys.exit(f"Unexpected Error occurred in fetching new access token: {err}")


if __name__ == '__main__':
    # 0. Prepare gmail service object to send gmail notifications
    gmail_service = gmail_utils.get_service(GMAIL_TOKEN_FILE, GMAIL_CREDENTIAL_FILE)

    # 1. Process arguments passed into the program
    parser = argparse.ArgumentParser(
        description="Script to check reddit every X minutes. "
                    "WANING: Make sure to check Reddit API's rate limits before "
                    "deciding on the input parameters, -m and -s, for this script.",
        formatter_class=argparse.RawTextHelpFormatter,
        usage=argparse.SUPPRESS)

    # On how to create list of list arguments for argparse, see
    # REF: https://stackoverflow.com/q/36166225
    parser.add_argument('-s', required=True, type=str, nargs='+',  # action='append',
                        help="Subreddit's name (e.g., r/gamesale/new)")
    parser.add_argument('-k', required=True, type=str, nargs='+',
                        help="Keyword to check in the posts (e.g., 'Megaman 11'). "
                             "Regular expression is okay.")
    parser.add_argument('-m', required=False, type=int, default=5,
                        help="How many minutes should each check be apart. "
                             "Default is checking once every 5 minutes.")
    parser.add_argument('-l', required=False, type=int, default=100,
                        help="Number of posts to search the keyword for. Default is 100.")
    args = parser.parse_args()

    # Get the very first Reddit access token.
    # From here on out, we'll only refresh the token when it expires.
    access_token, expires_on = generate_new_access_token(client_id, client_secret, username, pwd)
    keyword_last_post_name = {}
    while True:
        for subreddit in args.s:
            resource_url = ''.join([REDDIT_API_URL, subreddit])
            for keyword in args.k:
                cur_time = datetime.now()
                matching_posts = []
                access_token, expires_on = generate_new_access_token(client_id, client_secret,
                                                                     username, pwd,
                                                                     access_token, expires_on)

                if keyword not in keyword_last_post_name:
                    keyword_last_post_name[keyword] = ''

                # We can use 'before' parameter to grab posts that are not read by this script yet.
                # For that, the parameter should be like {'before': 't3_<id_of_the_last_post_we_have_seen>'}
                parameters = {'limit': args.l, 'before': keyword_last_post_name[keyword]}

                print(f"\n:::\nFetching {resource_url}"
                      f"\nto scan for keyword '{keyword}'"
                      f"\nat {cur_time}"
                      f"\nwith {parameters}\n:::\n")
                response = requests.get(resource_url,
                                        headers={"Authorization": f"bearer {access_token}",
                                                 "User-Agent": USER_AGENT},
                                        params=parameters)

                for i, post in enumerate(response.json()['data']['children']):
                    if i == 0:
                        # Reddit API returns the most recent post at index=0.
                        # We'll cache that in keyword_last_post_name for future pagination.
                        keyword_last_post_name[keyword] = post['data']['name']

                    post_id = post['data']['id']
                    post_name = post['data']['name']
                    post_created_utc = post['data']['created_utc']
                    title = post['data']['title']
                    post_text = post['data']['selftext']
                    post_url = post['data']['url']

                    if re.search(keyword, ''.join([title, post_text]), re.IGNORECASE):
                        print(f"\n{i}. Title: {title}")
                        print(f"{post_name}")
                        print(f"{post_text}\n===")
                        matching_posts.append({
                            '_title': title,
                            'post_url': post_url
                        })

                if matching_posts:
                    # Send email notification via Gmail API service
                    gmail_msg = gmail_utils.create_message(
                        sender_email,
                        ';'.join(recipient_emails),
                        f"Alert for {keyword} on {subreddit} at {cur_time}",
                        json.dumps(matching_posts, indent=4, sort_keys=True, separators=('<br>', ': '))
                    )
                    gmail_utils.send_message(gmail_service, 'me', gmail_msg)

                    # # Code below is when we want to write out the results in a file
                    # alert_msg = {'email_subject': f"Alert for {keyword} on {subreddit} at {cur_time}",
                    #              'email_body': matching_posts}
                    # file_name = '_'.join(['send_email_alert', datetime.now().strftime('%Y%m%d_%H%M%S'), '.json'])
                    # with open(file_name, 'w') as f:
                    #     json.dump(alert_msg, f, indent=4, sort_keys=True)

                    # IMPORTANT: Make sure to reset the matching_posts variable
                    matching_posts = []
                else:
                    print("\nFound no result.\n===")

        # After completing scan of every subreddit in the input parameter, take an X-minute break
        time.sleep(60 * args.m)
