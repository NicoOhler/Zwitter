# Simple Twitter-Clone API
# Author: Nico Ohler
# Date: 2022-09-10

# API on localhost:8000
# communicates with redis database hosted on railway.app
# https://railway.app/project/511e69e2-25d5-471a-b862-9e676ec5401c

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
from fastapi.middleware.cors import CORSMiddleware

# establish connection to redis
# decode_responses=True is needed to get strings instead of bytes
rdb = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# create FastAPI app
app = FastAPI()
# CORS middleware specifies allowed origins
app.add_middleware(CORSMiddleware,
                   allow_origins=ALLOWED_ORIGINS,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

# todo background task ==> reduce latency
# todo reply - reply:{tweet_id} -> [reply_id]
# todo transactional?
# todo none checks, error handling, etc.
# todo login
# todo pubsub for timeline
# todo user profile
# todo search - GET /search/{query}


def extract_hashtags(text):
    return list(set([word[1:] for word in text.split() if word.startswith("#")]))


def extract_mentions(text):
    return list(set([word[1:] for word in text.split() if word.startswith("@")]))


def prepare_tweet(tweet, user):
    if len(tweet["content"]) > CHARACTER_LIMIT:
        raise Exception("Tweet exceeds character limit")

    tweet["id"] = str(uuid.uuid4())
    tweet["username"] = user
    tweet["display_name"] = user
    tweet["created_at"] = time.time()
    tweet["like_count"] = 0
    tweet["reply_count"] = 0
    tweet["retweet_count"] = 0

    # extract unique hashtags and mentions
    # todo mention displayname
    # todo add link to hashtag and mention
    tweet["hashtags"] = extract_hashtags(tweet["content"])
    tweet["mentions"] = extract_mentions(tweet["content"])

    # remove mentions of users who do not exist
    for mention in tweet["mentions"]:
        if not rdb.get(f"profile:{user}"):
            tweet["mentions"].remove(mention)

    # recipients are unique followers and mentioned users
    tweet["recipients"] = list(set(tweet["mentions"] + list(rdb.smembers(f"followers:{user}"))))

    return tweet


# API endpoints
# get tweets
@app.get("/tweet")  # ?id={tweet_id},{tweet_id}
async def get_tweets(request: Request):
    ids = request.query_params.get("id").split(",")
    tweets = [rdb.get(f"tweet:{id}") for id in ids]
    return json.dumps(tweets)


# send tweet
@app.post("/tweet/{user}")
async def send_tweet(user: str, tweet: Request):

    tweet = prepare_tweet(await tweet.json(), user)
    tweet_id = tweet["id"]

    # todo start transaction
    # upload tweet
    rdb.set(f"tweet:{tweet_id}", json.dumps(tweet))

    # add tweet to user's user timeline
    rdb.lpush(f"user_timeline:{user}", tweet_id)

    # add tweet to each follower's home timeline
    for follower in tweet["recipients"]:
        rdb.lpush(f"home_timeline:{follower}", tweet_id)

    # track hashtags and mentions
    for hashtag in tweet["hashtags"]:
        rdb.sadd(f"hashtags:{hashtag}", tweet_id)
        rdb.sadd(f"hashtags", hashtag)

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
async def get_user_timeline(user: str, skip: int = SKIP_DEFAULT, limit: int = LIMIT_DEFAULT):
    timeline = []
    # get all tweets from user timeline
    tweet_ids = rdb.lrange(f"user_timeline:{user}", skip, limit - LIMIT_OFFSET)
    for tweet_id in tweet_ids:
        timeline.append(rdb.get(f"tweet:{tweet_id}"))
    return timeline


# show home timeline
@app.get("/timeline/{user}/home")
async def get_home_timeline(user: str, skip: int = SKIP_DEFAULT, limit: int = LIMIT_DEFAULT):
    timeline = []
    # get all tweets from home timeline
    tweet_ids = rdb.lrange(f"home_timeline:{user}", skip, limit - LIMIT_OFFSET)
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
    # differentiate between public and private profile
    return {"user": user}


# search - show n hashtags and m users
@app.get("/search/{query}")
async def search(query: str):
    # get hashtags starting with query
    hashtags = rdb.sscan_iter(f"hashtags", match=f"{query}*")
    # keep n most used hashtags
    hashtags = sorted(hashtags, key=lambda hashtag: rdb.scard(f"hashtags:{hashtag}"),
                      reverse=True)[:HASHTAGS_PER_SEARCH]

    # get users starting with query
    users = rdb.keys(f"profile:{query}*")
    # keep m most followed users
    users = sorted(users, key=lambda user: rdb.scard(f"followers:{user}"), reverse=True)[:USERS_PER_SEARCH]

    return {"hashtags": hashtags, "users": users}


# todo merge timeline and tweets lookup
# redis function?