import tweepy
import time
import os
from tweet_monitor import TweetMonitor
from user_evaluator import UserEvaluator
from vouch_checker import VouchChecker
from response_generator import ResponseGenerator
import logging

# Set up logging
logging.basicConfig(filename='trust_sentry.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load API credentials from environment variables
API_KEY = os.environ.get('API_KEY')
API_SECRET = os.environ.get('API_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

# Initialize Tweepy v2 client
api_client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Initialize bot components
monitor = TweetMonitor(api_client)
evaluator = UserEvaluator(api_client)
voucher = VouchChecker(api_client)
responder = ResponseGenerator(api_client)

def run_bot():
    logging.info("Starting Bot...")
    print("Bot initialized.")
    
    while True:
        try:
            # Fetch tweets with trigger phrase
            tweets = monitor.scan_for_mentions()
            if not tweets:
                logging.info("No relevant tweets detected. Pausing...")
                print("No tweets found. Retrying in 5 minutes...")
                time.sleep(300)
                continue

            for tweet in tweets:
                logging.info(f"Processing tweet ID: {tweet.id}")
                print(f"Analyzing tweet: {tweet.id}")

                # Get the original tweet’s author
                author_id = monitor.fetch_referenced_author(tweet)
                if not author_id:
                    logging.warning(f"No valid author for tweet {tweet.id}")
                    continue

                time.sleep(2)  # API call delay

                # Evaluate user trustworthiness
                metrics = evaluator.assess_profile(author_id)
                time.sleep(2)

                # Verify vouching by trusted accounts
                is_vouched = voucher.check_trust_status(author_id)
                metrics["is_vouched"] = is_vouched

                time.sleep(2)

                # Post response
                responder.post_assessment(tweet.id, metrics)
                logging.info(f"Posted response for tweet {tweet.id}")
                print(f"Responded to tweet {tweet.id}")

                time.sleep(10)  # Delay between tweets

        except tweepy.TooManyRequests:
            logging.error("Rate limit exceeded. Waiting 15 minutes.")
            print("Rate limit reached. Waiting 15 minutes...")
            time.sleep(900)
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            print(f"Error: {str(e)}. Retrying in 1 minute...")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()