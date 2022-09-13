# Simple Twitter-Clone API
# Author: Nico Ohler
# Date: 2022-09-10

# API on localhost:8000
# communicates with redis database

# packages: fastapi, uvicorn, redis
# specify redis url in redis_url.key
# start with: uvicorn api:app --reload

# todo move fastapi to railway.app
from config import *
import time
import uuid
import json
import redis
from fastapi import FastAPI, Request

# establish connection to redis
# decode_responses=True is needed to get strings instead of bytes
rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)
rdb_json = rdb.json()
rdb_text = rdb.ft()

# create FastAPI app
app = FastAPI()

# todo transactional?
# todo none checks, error handling, etc.
# todo login
# todo pubsub for timeline
# todo user profile
# todo search tweets - GET /search/{query}


def extract_hashtags(text):
    return list(set([word[1:] for word in text.split() if word.startswith("#")]))


def extract_mentions(text):
    return list(set([word[1:] for word in text.split() if word.startswith("@")]))


def prepare_tweet(tweet, user):
    tweet["id"] = str(uuid.uuid4())
    tweet["from"] = user
    tweet["time"] = time.time()
    tweet["likes"] = 0
    tweet["retweets"] = 0

    # extract unique hashtags and mentions
    # todo add link to hashtag and mention
    tweet["hashtags"] = extract_hashtags(tweet["content"])
    tweet["mentions"] = extract_mentions(tweet["content"])

    # remove mentions of users who do not exist
    for mention in tweet["mentions"]:
        if not rdb.get(f"profile:{user}"):
            tweet["mentions"].remove(mention)

    # recipients are unique followers and mentioned users
    tweet["recipients"] = list(set(tweet["mentions"] + rdb.smembers(f"followers:{user}")))


# API endpoints
# send tweet
@app.post("/tweet/{user}")
async def send_tweet(user: str, tweet: Request):

    tweet = prepare_tweet(await tweet.json(), user)
    tweet_id = tweet["id"]

    # todo start transaction
    # upload tweet
    rdb.set("tweet:{tweet_id}", json.dumps(tweet))

    # add tweet to user's user timeline
    rdb.lpush(f"user_timeline:{user}", tweet_id)

    # add tweet to each follower's home timeline
    for follower in tweet["recipients"]:
        rdb.lpush(f"home_timeline:{follower}", tweet_id)

    # track hashtags and mentions
    for hashtag in tweet["hashtags"]:
        rdb.sadd(f"hashtags:{hashtag}", tweet_id)

    for mention in tweet["mentions"]:
        rdb.sadd(f"mentions:{mention}", tweet_id)

    # todo end transaction


# delete tweet
@app.delete("/tweet/{user}/{tweet_id}")
async def delete_tweet(user: str, tweet_id: str):
    # todo start transaction
    # remove tweet from user's user timeline
    rdb.lrem(f"user_timeline:{user}", 0, tweet_id)

    # get time of sending
    tweet = json.loads(rdb.get(f"tweet:{tweet_id}"))

    # remove tweet from each recipient's home timeline
    # unless tweet is too old
    if time.time() - tweet["time"] < TTL:
        for recipient in tweet["recipients"]:
            rdb.lrem(f"home_timeline:{recipient}", 0, tweet_id)

    for hashtag in tweet["hashtags"]:
        rdb.srem(f"hashtags:{hashtag}", tweet_id)

    for mention in tweet["mentions"]:
        rdb.srem(f"mentions:{mention}", tweet_id)

    # todo end transaction


# show user timeline
@app.get("/timeline/{user}/user")
async def show_user_timeline(user: str, skip: int = SKIP_DEFAULT, limit: int = LIMIT_DEFAULT):
    timeline = []
    # get all tweets from user timeline
    tweet_ids = rdb.lrange(f"{user}:user_timeline", skip, limit - LIMIT_OFFSET)
    for tweet_id in tweet_ids:
        timeline.append(rdb.get(f"tweet:{tweet_id}"))
    return timeline


# show home timeline
@app.get("/timeline/{user}/home")
async def show_home_timeline(user: str, skip: int = SKIP_DEFAULT, limit: int = LIMIT_DEFAULT):
    timeline = []
    # get all tweets from home timeline
    tweet_ids = rdb.lrange(f"{user}:home_timeline", skip, limit - LIMIT_OFFSET)
    for tweet_id in tweet_ids:
        timeline.append(rdb.get(f"tweet:{tweet_id}"))
    return timeline


# follow user
@app.post("/follower/{user}/{follower}")
async def follow_user(user: str, follower: str):
    # add follower to user's followers
    rdb.sadd(f"followers:{user}", follower)
    # ? add user to follower's profile


# unfollow user
@app.delete("/follower/{user}/{follower}")
async def unfollow_user(user: str, follower: str):
    # remove follower from user's followers
    rdb.srem(f"followers:{user}", follower)
    # ? remove user from follower's profile


# show followers
@app.get("/follower/{user}")
async def show_followers(user: str):
    # get user's followers
    followers = rdb.smembers(f"followers:{user}")
    return followers


# show user profile - GET /user/{user}
@app.get("/user/{user}")
async def show_user_profile(user: str):
    # todo
    return {"user": user}
