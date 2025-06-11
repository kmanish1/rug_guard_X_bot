

It is a Python-powered X bot that assesses the trustworthiness of a tweet's original author when triggered by the phrase "@blink_vault riddle me this" in a reply. Built for seamless deployment on Replit, it uses a modular design with robust error handling and logging for reliability.

## Getting Started

### Requirements
- X Developer account with API credentials (sign up at https://developer.x.com).
- Replit account for hosting and deployment.
- Python 3.8+ with dependencies listed in `requirements.txt`.

### Setup Guide
1. **Clone the Project**:
   - Create a new repository on GitHub and clone it locally.
   - Copy the bot’s files into your repository.

2. **Install Dependencies**:
   - Ensure `requirements.txt` is in your project root.
   - Run `pip install -r requirements.txt` locally or let Replit handle it automatically.

3. **Configure Environment Variables**:
   - Create a `.env` file in the project root with the following:
     ```plaintext
     API_KEY=your_api_key
     API_SECRET=your_api_secret
     ACCESS_TOKEN=your_access_token
     ACCESS_TOKEN_SECRET=your_access_token_secret
     BEARER_TOKEN=your_bearer_token
     ```
   - On Replit, add these as Secrets (see deployment steps below).

4. **Set Up Trusted Accounts**:
   - Open `vouch_checker.py` and replace the `trusted_ids` list with all user IDs from the trust list: https://github.com/devsyrem/turst-list/blob/main/list.
   - Ensure every ID from the list is included to meet bounty requirements.

5. **Launch the Bot**:
   - Deploy on Replit (see deployment section below).
   - The bot will monitor X for the trigger phrase and respond with trust reports.

## Project Structure
- `bot_core.py`: Core logic that runs the bot and ties components together.
- `tweet_monitor.py`: Scans for the trigger phrase and identifies the original author.
- `user_evaluator.py`: Analyzes user profiles for trustworthiness metrics.
- `vouch_checker.py`: Validates if trusted accounts vouch for the user.
- `response_generator.py`: Crafts and posts trust assessment replies.
- `api_handler.py`: Handles X API calls with retry logic for rate limits.
- `requirements.txt`: Lists dependencies (`tweepy==4.14.0`, `requests`).
- `trust_sentry.log`: Logs bot activity for debugging.

## Key Features
- Detects "@blink_vault riddle me this" in replies and evaluates the original tweet’s author.
- Uses custom metrics (account age, follower ratio, bio, engagement) for trust scoring.
- Verifies vouching by 3+ trusted accounts from the provided list.
- Posts concise trust reports with a unique scoring system.
- Logs all actions to `trust_sentry.log` for easy monitoring.

## Deployment on Replit
1. Create a new Replit project (Python template).
2. Upload all files (or import from GitHub; see GitHub section).
3. In Replit’s “Secrets” tab (lock icon), add the `.env` variables:
   - `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, `ACCESS_TOKEN_SECRET`, `BEARER_TOKEN`.
4. Click “Run” to start the bot. It will continuously monitor X.

## Notes
- The bot uses the free X API v2 tier (up to 1,500 posts/month).
- Update `trusted_ids` in `vouch_checker.py` with the full list from the GitHub trust list.
- Rate limit handling ensures the bot retries after delays, preventing crashes.

## Troubleshooting
- If the bot fails to post, verify API credentials and rate limits.
- Check `trust_sentry.log` for detailed error messages.