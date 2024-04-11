#!/bin/bash

source venv/bin/activate 
source .env
printf "Environment activated\n"

pip install tweepy openai python-dotenv
printf "Dependencies installed\n"

pip3 freeze > requirements.txt
pip3 install --upgrade --target ./package -r requirements.txt
printf "Dependencies packaged\n"

cd package
zip -r ../deployment-package.zip .
printf "Package zipped\n"

cd ..
zip -g deployment-package.zip dailyAffirmations.py friends.json emotions.json prev_tweets.json gptRole.txt dates/*
printf "Files zipped\n"
printf "Deployment package ready\n"

aws s3 cp deployment-package.zip "s3://$S3_BUCKET_NAME/"
printf "Package uploaded to S3\n"

aws lambda update-function-code --function-name $FUNCTION_NAME --s3-bucket $S3_BUCKET_NAME --s3-key deployment-package.zip
printf "Lambda function updated\n"

deactivate
