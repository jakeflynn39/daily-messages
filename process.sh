#!/bin/bash

source venv/bin/activate
printf "Environment activated\n"
pip install tweepy openai python-dotenv
printf "Dependencies installed\n"
pip3 freeze > requirements.txt
pip3 install --target ./package -r requirements.txt
printf "Dependencies packaged\n"
cd package
zip -r ../deployment-package.zip .
printf "Package zipped\n"
cd ..
zip -g deployment-package.zip dailyAffirmations.py friends.json prev_tweets.json gptRole.txt
printf "Files zipped\n"
printf "Deployment package ready\n"
