from datetime import datetime
import tweepy

class UserEvaluator:
    def __init__(self, api_client):
        self.api_client = api_client

    def assess_profile(self, user_id):
        try:
            # Fetch user profile details
            user_data = self.api_client.get_user(
                id=user_id,
                user_fields=["created_at", "public_metrics", "description"]
            )
            if not user_data.data:
                return {"error": "Unable to fetch user data"}

            # Get user’s recent tweets
            recent_tweets = self.api_client.get_users_tweets(
                id=user_id,
                tweet_fields=["public_metrics"],
                max_results=10
            )

            # Calculate account age
            profile_age = (datetime.now() - user_data.data.created_at).days

            # Compute follower-to-following ratio
            stats = user_data.data.public_metrics
            follower_ratio = stats["followers_count"] / (stats["following_count"] + 1)

            # Analyze bio content
            bio_text = user_data.data.description or ""
            bio_char_count = len(bio_text)
            risky_terms = any(term in bio_text.lower() for term in ["scam", "fake", "legit"])

            # Evaluate tweet engagement
            like_avg, retweet_avg = 0, 0
            if recent_tweets.data:
                likes = [t.public_metrics["like_count"] for t in recent_tweets.data]
                retweets = [t.public_metrics["retweet_count"] for t in recent_tweets.data]
                like_avg = sum(likes) / len(likes)
                retweet_avg = sum(retweets) / len(retweets)

            return {
                "profile_age_days": profile_age,
                "follower_ratio": follower_ratio,
                "bio_length": bio_char_count,
                "has_risky_terms": risky_terms,
                "average_likes": like_avg,
                "average_retweets": retweet_avg,
                "content_score": 0.6  # Adjusted neutral score
            }

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}