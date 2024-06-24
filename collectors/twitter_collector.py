import tweepy
from config import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET

def collect_tweets(list_id):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    tweets = []
    for tweet in tweepy.Cursor(api.list_timeline, list_id=list_id).items(10):
        tweets.append({
            'title': f"Tweet from {tweet.author.name}",
            'text': tweet.text,
            'link': f"https://twitter.com/{tweet.author.screen_name}/status/{tweet.id}",
            'source': 'Twitter'
        })
    return tweets