# Simple Twitter-Clone API
# Author: Nico Ohler
# Date: 2022-09-10

# API on localhost:8000
# communicates with redis database

# packages: fastapi, uvicorn, redis
# specify redis url in redis_url.key
# start with: uvicorn twitter_api:app --reload

# todo move fastapi to railway.app
from re import I
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

# sample tweet
tweet = {
    "id": "86d65a60-3c13-4980-8255-84715e1f6b6e",
    "from": "aigner",
    "sent": 1662806699.5619178,
    "content": "waduttn @riedl #waduttn",
    "likes": 0,
    "retweets": 0,
    "mentions": ["riedl"],
    "hashtags": ["#waduttn"],
    "recipients": ["riedl", "kurz"],
}


async def add_tweet_to_hashtags(hashtags, tweet_id):
    for hashtag in hashtags:
        rdb.sadd(f"hashtag:{hashtag}", tweet_id)


async def add_tweet_to_mentions(mentions, tweet_id):
    for mention in mentions:
        rdb.sadd(f"mention:{mention}", tweet_id)


# API endpoints
# send tweet
@app.post("/tweet/{user}")
async def send_tweet(user: str, tweet: Request):
    tweet = await tweet.json()
    tweet["id"] = str(uuid.uuid4())
    tweet["from"] = user
    tweet["sent"] = time.time()
    tweet = json.dumps(tweet)

    # start transaction
    pipe = rdb.pipeline(transaction=True)
    pipe.multi()

    # add tweet to user's user timeline
    rdb.lpush(f"{user}:user_timeline", tweet)

    # add tweet to followers' home timelines
    followers = rdb.smembers(f"{user}:followers")
    for follower in followers:
        rdb.lpush(f"{follower}:timeline", tweet)

    # execute transaction
    pipe.execute()
    return f"Tweet sent from {user}"


# delete tweet
@app.delete("/tweet/{user}/{tweet_id}")
async def delete_tweet(user: str, tweet_id: str):
    # start transaction
    pipe = rdb.pipeline(transaction=True)
    pipe.multi()

    # todo
    # remove tweet from user's user timeline
    # remove tweet from followers' home timelines

    # execute transaction
    pipe.execute()
    return {"message": "Tweet deleted"}


# show user timeline
@app.get("/timeline/{user}/user")
async def show_user_timeline(user: str, skip: int = SKIP_DEFAULT, limit: int = LIMIT_DEFAULT):
    # get user's user timeline
    timeline = rdb.lrange(f"{user}:user_timeline", skip, limit - LIMIT_OFFSET)
    return timeline


# show home timeline
@app.get("/timeline/{user}/home")
async def show_home_timeline(user: str, skip: int = SKIP_DEFAULT, limit: int = LIMIT_DEFAULT):
    # get user's timeline
    timeline = rdb.lrange(f"{user}:timeline", skip, limit - LIMIT_OFFSET)
    return timeline


# follow user
@app.post("/follower/{user}/{follower}")
async def follow_user(user: str, follower: str):
    # add follower to user's followers
    rdb.sadd(f"{user}:followers", follower)
    # ? add user to follower's profile

    return f"{follower} is now following {user}"


# unfollow user
@app.delete("/follower/{user}/{follower}")
async def unfollow_user(user: str, follower: str):
    # remove follower from user's followers
    rdb.srem(f"{user}:followers", follower)
    # ? remove user from follower's profile

    return f"{follower} is no longer following {user}"


# show followers
@app.get("/follower/{user}")
async def show_followers(user: str):
    # get user's followers
    followers = rdb.smembers(f"{user}:followers")
    return followers


# show user profile - GET /user/{user}
@app.get("/user/{user}")
async def show_user_profile(user: str):
    return {"user": user}
