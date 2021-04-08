# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from time import sleep
import requests
import csv

TWEETS_QUERY_PARAM = {
      "include_profile_interstitial_type": "1",
      "include_blocking": "1",
      "include_blocked_by": "1",
      "include_followed_by": "1",
      "include_want_retweets": "1",
      "include_mute_edge": "1",
      "include_can_dm": "1",
      "include_can_media_tag": "1",
      "skip_status": "1",
      "cards_platform": "Web-12",
      "include_cards": "1",
      "include_composer_source": True,
      "include_ext_alt_text": True,
      "include_reply_count": "1",
      "tweet_mode": "extended",
      "include_entities": True,
      "include_user_entities": True,
      "include_ext_media_color": True,
      "include_ext_media_availability": True,
      "send_error_codes": True,
      "simple_quoted_tweets": True,
      "include_tweet_replies": True,
      "count": "20",
      "ext": "mediaStats,highlightedLabel,cameraMoment"
}

class TwitterSpider:
    __headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "en",
        }

    __tweets_url = "https://twitter.com/i/api/2/timeline/profile/%s.json?%s"

    def __init__(
        self,
        csrf_token: str,
        authorization: str,
        username: str,
        cookie:str,
        tweets_limit: int = 0,
        request_delay: int = 2,
        retweets: bool = False
    ):
        self.username = username.lower()
        self.req_session = requests.Session()
        self.scraped_tweets = 0
        self.tweets_limit = tweets_limit
        self.request_delay = request_delay
        self.retweets = retweets

        self.__headers["x-csrf-token"] = csrf_token
        self.__headers["authorization"] = authorization
        self.__headers["cookie"] = cookie

        out_file = open(
            "%s.csv" % username, 
            'w+', 
            newline='\n', 
            encoding='utf-8'
        )

        self.csv_wr = csv.writer(out_file, quoting=csv.QUOTE_ALL)
        self.csv_wr.writerow([
            "Full text",
            "reply_count",
            "favorite_count",
            "retweet_count",
            "created_at"
        ])

        self.tweets_query_params = TWEETS_QUERY_PARAM


    def username_to_user_id(self):
        """
        Returns the twitter user id from username
        """
        query_params = {
            "variables": {
                "screen_name": self.username,
                "withHighlightedLabel": True
            }
        }

        user_id_url = f'https://twitter.com/i/api/graphql/hc-pka9A7gyS3xODIafnrQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{self.username}%22%2C%22withHighlightedLabel%22%3Atrue%7D'
        user_id_url = user_id_url.replace("%27", "%22").replace("True", "true")

        resp = self.req_session.get(
            url = user_id_url,
            headers = self.__headers
        )
        try:
            data = resp.json()['data']
            item = {}
            user_id = data['user']['rest_id']
            item['rest_id'] = user_id
            item['des'] = data['user']['affiliates_highlighted_label']['label']['description']
            item['created_at'] = data['user']['legacy']['created_at']
            item['description'] = data['user']['legacy']['description']
            item['followers_count'] = data['user']['legacy']['followers_count']
            item['friends_count'] = data['user']['legacy']['friends_count']
            item['listed_count'] = data['user']['legacy']['listed_count']
            item['media_count'] = data['user']['legacy']['media_count']
            print(item)
        except Exception as e:
            print(e)
            return
        return user_id


    def get_tweets(self, userId: str, nextCursor: str = None):
        self.tweets_query_params['userId'] = userId

        """
        Twitter uses cursors as pagination.
        If a cursor has been found, it is being added to the 
        query string parameters
        """
        if nextCursor:
            self.tweets_query_params['cursor'] = nextCursor

        tweets_list_url = self.__tweets_url % (
            self.tweets_query_params['userId'],
            urlencode(self.tweets_query_params)
        )
        print(tweets_list_url)
        resp = self.req_session.get(
            url = tweets_list_url,
            headers = self.__headers
        )
        try:
            tweets = resp.json()['globalObjects']['tweets']
        except Exception as e:
            print(e, "was not found")
            return

        """
        Parsing tweets
        """
        for ind, tweet in enumerate(tweets):
            if not self.retweets:
                if self.tweets_query_params['userId'] != tweets[tweet]["user_id_str"]:
                    continue

            self.csv_wr.writerow([
                tweets[tweet]["full_text"],
                tweets[tweet]["reply_count"],
                tweets[tweet]["favorite_count"],
                tweets[tweet]["retweet_count"],
                tweets[tweet]["created_at"]
            ])
            print("New tweet added with id: %s" % (
                tweets[tweet]['id_str'],)
            )

            self.scraped_tweets += 1

        """
        Searching for next page cursor id
        """
        entries = resp.json()['timeline']['instructions'][0]['addEntries']['entries']
        
        for entry in entries:
            try:
                cursor = entry['content']['operation']['cursor']
            except:
                continue

            if cursor['cursorType'] == "Bottom":
                nextCursor = cursor['value']
                print("Found new cursor: %s" % (nextCursor,))
                break

        if self.scraped_tweets >= self.tweets_limit and self.tweets_limit != 0:
            return
        else:
            if len(tweets) > 0 and nextCursor:
                sleep(self.request_delay)
                return self.get_tweets(userId, nextCursor)
            return