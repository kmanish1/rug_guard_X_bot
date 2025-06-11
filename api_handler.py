import time
import tweepy

def execute_api_request(api_func, *args, retries=3, **kwargs):
    """
    Execute API request with retry logic for handling rate limits.
    """
    for i in range(retries):
        try:
            return api_func(*args, **kwargs)
        except tweepy.TooManyRequests:
            if i < retries - 1:
                delay = (2 ** i) * 60
                print(f"Rate limit encountered. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries exhausted for API request.")
                raise
        except Exception as e:
            print(f"API error: {str(e)}")
            if i < retries - 1:
                time.sleep(5)
            else:
                raise
    return None