import re
import json
import requests
from urllib.parse import urlencode
from urllib.parse import quote
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from loguru import logger


proxies = {'https': 'http://127.0.0.1:15732'} # VPN

def get_infos():
    url = "https://abs.twimg.com/responsive-web/client-web/main.8644ab25.js"
    logger.debug('开始获取infos...')
    response = requests.get(url, proxies=proxies, verify=False)
    authorization = "Bearer " + re.search("(AAAAA.*?)\"", response.text).group(1)
    user_tweets = re.search('queryId:\"(.{22})\",operationName:\"TweetDetail\",', response.text).group(1)
    user_by_screen_name = re.search('queryId:\"(.{22})\",operationName:\"UserByScreenName\",', response.text).group(1)
    gt_headers = {
        'authority': 'api.twitter.com',
        'content-length': '0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'x-twitter-client-language': 'zh-cn',
        'sec-ch-ua-mobile': '?0',
        'authorization': authorization,
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.99 Safari/537.36',
        'x-twitter-active-user': 'yes',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'origin': 'https://twitter.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://twitter.com/',
        'accept-language': 'zh-CN,zh;q=0.9',
    }
    logger.debug('开始获取guest_token...')
    response_gt = requests.post('https://api.twitter.com/1.1/guest/activate.json', proxies=proxies, headers=gt_headers,verify=False)
    return dict(
        guest_token=response_gt.json()['guest_token'],
        authorization=authorization,
        user_tweets=user_tweets,
        user_by_screen_name=user_by_screen_name
    )
infos = get_infos()


class TwitterBase():
    def __init__(self):
        self.infos = infos

    def get_headers(self, **kwargs):
        return {
            'x-guest-token': self.infos['guest_token'],
            'authorization': self.infos['authorization'],
            'authority': 'twitter.com',
            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            'x-twitter-client-language': 'zh-cn',
            'sec-ch-ua-mobile': '?0',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/97.0.4692.99 Safari/537.36',
            'x-twitter-active-user': 'yes',
            'sec-ch-ua-platform': '"Windows"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://twitter.com/nytimes/status/%s?'.format(kwargs['focalTweetId']),
            'accept-language': 'zh-CN,zh;q=0.9',
        }


class TwitterComment(TwitterBase):
    Uri = 'https://twitter.com/i/api/graphql/{}/TweetDetail?'
    def get_url(self, **kwargs):
        variables = {"focalTweetId": kwargs['focalTweetId'], "with_rux_injections": False,
                     "includePromotedContent": True, "withCommunity": True,
                     "withQuickPromoteEligibilityTweetFields": True, "withBirdwatchNotes": False,
                     "withSuperFollowsUserFields": True, "withDownvotePerspective": False,
                     "withReactionsMetadata": False, "withReactionsPerspective": False,
                     "withSuperFollowsTweetFields": True, "withVoice": True, "withV2Timeline": True}
        features = {"unified_cards_follow_card_query_enabled": False, "dont_mention_me_view_api_enabled": True,
                    "interactive_text_enabled": True, "responsive_web_uc_gql_enabled": True, "vibe_api_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True, "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                    "responsive_web_enhance_cards_enabled": True}
        data = {
            "variables": variables,
            "features": features
        }
        params_data = urlencode(data).replace('+', '').replace('%27','%22').replace('True','true').replace('False','false')

        if 'cursor' in kwargs and kwargs['cursor']:
            variables.update({'cursor':kwargs['cursor'],'referrer':'tweet'})

        url = self.Uri.format(self.infos['user_tweets']) + params_data
        return url


def requestCM(focalTweetId,cursor=None):
    get_guess_url = twg.get_url(focalTweetId=focalTweetId,cursor=cursor)
    get_guess_headers = twg.get_headers(focalTweetId=focalTweetId)
    print(get_guess_url)
    guess_response = requests.get(url=get_guess_url, headers=get_guess_headers, verify=False,proxies=proxies).text
    print(guess_response)
    cursor = parse_response(guess_response)
    return cursor



def parse_response(twitter_content):
    print(twitter_content)
    cursor = None
    instructions = None

    logger.debug(f"下一页cursor:{cursor}")
    return cursor



if __name__ == '__main__':
    focalTweetId = '1562527919527800832'
    twg = TwitterComment()
    logger.debug(f"focalTweetId:{focalTweetId}")

    cursor = requestCM(focalTweetId)
    while 1:
        if cursor:
            cursor = requestCM(focalTweetId,cursor)
        else:
            break
