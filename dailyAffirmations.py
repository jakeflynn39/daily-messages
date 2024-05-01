import openai
import tweepy
import random
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import urllib.request

# load .env and keys for AWS Lambda
# CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
# CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
# ACCESS_TOKEN_KEY = os.environ.get('ACCESS_TOKEN_KEY')
# ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
# openai.api_key = os.environ.get('OPENAI_API_KEY')

# load .env and keys for local testing
load_dotenv()
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
openai.api_key = os.getenv('OPENAI_API_KEY')


def handler(event, context):
    today = datetime.today().strftime('%Y-%m-%d')

    image_location_local = None
    media_ids = None
    tweet = None
    create_image = False
    image_url = None

    if os.path.isfile(f'dates/{today}.txt'):
        with open(f'dates/{today}.txt', 'r') as file:
            tweet = file.read()

    else:
        with open('gptRole.txt', 'r') as file:
            role = file.read()
        with open('prev_tweets.json', 'r') as file:
            prev_tweets = json.load(file)["prevTweets"]

        with open('friends.json', 'r') as file:
            friends = json.load(file)["friends"]

        # get emotions.json
        with open('emotions.json', 'r') as file:
            emotions = json.load(file)["emotions"]

        emotion = random.choice(emotions)

        role = role.replace('***INSERT EMOTION HERE***', emotion)

        messages = [
            {
                "role": "system", 
                "content": role
            }, 
        ]

        tweet_directive = f'''Here are some of my previous tweets that I want you to learn from in json format: \n{prev_tweets}\n
            You can write between 2-3 sentences as long as you follow the same tone as my previous tweets and talk only about the friend I am providing here. 
            Make sure to include my dry humor, sarcasm, irony, and occasional self deprication, as well as subtle mis-spells and blatent refusal to follow 
            grammatical conventions, and mix up how you start the tweets so they do not all begin with 'Just' every time. \n** VERY IMPORTANT ** 
            Remember, mis-spell a word or 2, but do it subtlely, and include my subtle digs and sarcasm.\n Here is the description of 
            my friend I want you to tweet about: '''


        # choose friend but allow me to x out bios that I don't want to use
        while True:
            chosen_friend = random.choice(friends)

            if not all(bio.startswith('x') for bio in chosen_friend['bio']):
                break

        while True:
            bio = random.choice(chosen_friend['bio'])

            if not bio.startswith('x'):
                break

        friend_info = f"\nName: {chosen_friend['name']}\nHandle: {chosen_friend['handle']}\nBio: {bio}\n"

        image_location_local = chosen_friend.get('image_url', None)

        print(friend_info)

        # set gpt prompt
        messages.append({"role": "user", "content": tweet_directive + friend_info})

        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            temperature=1.09,
        )

        tweet = clean_up(response["choices"][0]["message"]["content"])

    print(tweet)

    # twitter api
    client = tweepy.Client(consumer_key=CONSUMER_KEY,
                        consumer_secret=CONSUMER_SECRET,
                        access_token=ACCESS_TOKEN_KEY,
                        access_token_secret=ACCESS_TOKEN_SECRET)
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    
    if not image_location_local and os.path.isfile(f'dates/images/{today}.jpeg'):
        image_location_local = f'dates/images/{today}.jpeg'

    if create_image:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=friend_info,
            size="1024x1024",
            quality="standard",
            n=1,
        )
    
        image_url = response.data[0].url

    if image_location_local:
        media = api.media_upload(image_location_local)
        media_ids = [media.media_id]

    if image_url:
        media = api.media_upload(urllib.request.urlretrieve(image_url)[0])
        media_ids = [media.media_id]

    # post tweet
    response = client.create_tweet(text=tweet, media_ids=media_ids)

def clean_up(tweet):
    tweet = tweet.replace('Tweet: ', '')
    if tweet[0] == '“' or tweet[0] == '"':
        tweet = tweet[1:]
    if tweet[-1] == '”' or tweet[-1] == '"':
        tweet = tweet[:-1]
    if tweet[0] == '@':
        tweet = '.' + tweet

    if len(tweet) < 270 and is_logan_webb_pitching_today():
        tweet += ' #HappyLWD'

    return tweet

def is_logan_webb_pitching_today():
    try:
        today = datetime.today().strftime('%Y-%m-%d')

        url = f'https://statsapi.mlb.com/api/v1/schedule?sportId=1,51&date={today}&language=en&hydrate=team(league),venue(location,timezone),linescore(matchup,runners,positions),decisions,homeRuns,probablePitcher,flags,review,seriesStatus,person,stats,broadcasts(all),game(tickets,atBatPromotions,content(media(epg),highlights(highlights),limit%3D4)),liveLookin'
        response = requests.get(url)

        data = response.json()

        for game in data["dates"][0]["games"]:
            for team in game["teams"]:
                if game["teams"][team]["probablePitcher"]["id"] == 657277:
                    return True
    except:
        pass
                
    return False

if __name__ == "__main__":
    handler(None, None)
