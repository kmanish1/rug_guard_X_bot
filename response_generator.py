class ResponseGenerator:
    def __init__(self, api_client):
        self.api_client = api_client

    def post_assessment(self, tweet_id, metrics):
        if "error" in metrics:
            message = "Error: User analysis unavailable."
        else:
            # Calculate trust score with new weights
            trust_score = 50
            if metrics["profile_age_days"] > 180:
                trust_score += 15
            if metrics["follower_ratio"] > 1.5:
                trust_score += 12
            if not metrics["has_risky_terms"]:
                trust_score += 8
            if metrics["average_likes"] > 3:
                trust_score += 10
            if metrics["is_vouched"]:
                trust_score += 25

            message = (
                f"Trust Score: {trust_score}/100\n"
                f"Account Age: {metrics['profile_age_days']} days\n"
                f"Follower Ratio: {metrics['follower_ratio']:.2f}\n"
                f"Vouched: {'Yes' if metrics['is_vouched'] else 'No'}"
            )

        self.api_client.create_tweet(text=message, in_reply_to_tweet_id=tweet_id)