from twitter_spider import TwitterSpider


def main(index_url):
    username = index_url.split('com/')[1]

    s = TwitterSpider(
        username=username,
        csrf_token="",
        authorization="",
        cookie = ''
    )
    # 先从 api/graphql 获取 rest_id
    rest_id = s.username_to_user_id()
    # 然后通过 rest_id 采集tuite列表
    s.get_tweets(rest_id)


if __name__ == '__main__':
    main(index_url = 'https://twitter.com/POTUS')
