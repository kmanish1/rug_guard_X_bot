from api_handler import execute_api_request

class TweetMonitor:
    def __init__(self, api_client):
        self.api_client = api_client
        self.trigger = "@blink_vault riddle me this"

    def scan_for_mentions(self):
        # Search for mentions of @blink_vault
        search_query = "@blink_vault -is:retweet"
        results = execute_api_request(
            self.api_client.search_recent_tweets,
            query=search_query,
            tweet_fields=["referenced_tweets", "author_id"],
            max_results=10
        )
        if not results or not results.data:
            return []

        # Filter for trigger phrase
        return [t for t in results.data if self.trigger.lower() in t.text.lower()]

    def fetch_referenced_author(self, tweet):
        if not hasattr(tweet, 'referenced_tweets') or not tweet.referenced_tweets:
            return None
        ref_tweet_id = tweet.referenced_tweets[0].id
        tweet_data = execute_api_request(
            self.api_client.get_tweet,
            ref_tweet_id,
            user_fields=["id"]
        )
        return tweet_data.data.author_id if tweet_data and tweet_data.data else None