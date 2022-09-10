# Simple Twitter-Clone API

# requirements: fastapi, uvicorn, redis
# start with: uvicorn twitter_api:app --reload

import time
import uuid
import json
import redis
from fastapi import FastAPI, Request

REDIS_URL_FILE = "redis_url.key"  # file with redis url
with open(REDIS_URL_FILE) as file:  # read redis url from file
    REDIS_URL = file.read()

SKIP_DEFAULT = 0  # skips first 0 tweets for /timeline
LIMIT_DEFAULT = 10  # limits to 10 tweets for /timeline
LIMIT_OFFSET = 1  # offset for /timeline because redis is 0-indexed?

# establish connection to redis
# decode_responses=True is needed to get strings instead of bytes
rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# create FastAPI app
app = FastAPI()

# todo none checks, error handling, etc.
# todo login
# todo async
# todo search tweets - GET /search/{query}


# API endpoints
# send tweet
@app.post("/tweet/{user}")
async def send_tweet(user: str, tweet: Request):
    tweet = await tweet.json()
    tweet["id"] = str(uuid.uuid4())
    tweet["from"] = user
    tweet["sent"] = time.time()
    tweet = json.dumps(tweet)

    # add tweet to user's user timeline
    rdb.lpush(f"{user}:user_timeline", tweet)

    # add tweet to followers' home timelines
    followers = rdb.smembers(f"{user}:followers")
    for follower in followers:
        rdb.lpush(f"{follower}:timeline", tweet)
    return f"Tweet sent from {user}"


# delete tweet
@app.delete("/tweet/{user}/{tweet_id}")
async def delete_tweet(user: str, tweet_id: str):
    # remove tweet from user's user timeline
    # remove tweet from followers' home timelines
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
