# Twitter Bot with GPT-3 Integration

This is a Twitter bot script that leverages OpenAI's GPT-3 model to generate tweets. The bot selects a random friend from a list and creates a tweet in a specified style. The bot also retrieves a predefined system message.

## Prerequisites

Before running the script, make sure you have the following set up:

- Twitter Developer API keys for authentication
- OpenAI API key
- Python environment with required packages (tweepy, openai, dotenv)

## Getting Started

1. Clone the repository or download the script.

2. Install the required Python packages using `pip`:

   ```bash
   pip install tweepy openai python-dotenv
   ```

3. Create a `.env` file in the same directory as the script and add the necessary environment variables:

   ```dotenv
   CONSUMER_KEY=your_twitter_consumer_key
   CONSUMER_SECRET=your_twitter_consumer_secret
   ACCESS_TOKEN_KEY=your_twitter_access_token_key
   ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Adjust the code to specify your environment variables. You can choose to load environment variables from `.env` for local testing or directly set them in the code for AWS Lambda deployment.

5. Create a `friends.json` file in the same directory as the script and add your friends' Twitter handles. You can reference `EXAMPLE_friends.json` for the format.

6. Create a `prev_tweets.json` file in the same directory as the script. This file is used so GPT can get a sense of your previous tweets and create messages in your style. You can reference `EXAMPLE_prev_tweets.json` for the format.

## Usage

### Local Testing

If you want to test the script locally, uncomment the lines that load environment variables locally from `.env` and comment out the lines that directly set the variables for AWS.

```python
# load .env and keys for local testing
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
openai.api_key = os.getenv('OPENAI_API_KEY')
```

### AWS Lambda Deployment

To deploy this script as an AWS Lambda function, ensure you set your environment variables directly in the code, and package the script along with the necessary dependencies into a deployment package.

To create the deployment package, run the following commands:

```bash
source venv/bin/activate
pip install tweepy openai python-dotenv
pip3 freeze > requirements.txt
pip3 install --target ./package -r requirements.txt
cd package
zip -r ../deployment-package.zip .
cd ..
zip -g deployment-package.zip dailyAffirmations.py friends.json prev_tweets.json gptRole.txt
```

Then, upload the `deployment-package.zip` file to AWS Lambda. Make sure to set the handler to `dailyAffirmations.lambda_handler` and set up the enviorment variables. Then set up Lambda triggers to run the script whenever you want.

## Execution

The script can be executed either locally for testing or deployed as an AWS Lambda function. When executed, it generates a tweet using GPT-3 and posts it to Twitter.
