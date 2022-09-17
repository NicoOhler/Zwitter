REDIS_URL_FILE = "api/redis_url.key"  # file with redis url
REDIS_URL_FILE = "redis_url.key"  # file with redis url
with open(REDIS_URL_FILE) as file:  # read redis url from file
    REDIS_URL = file.read()

# URLs allowed to access the API (CORS)
# todo change to railway.app
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]

# timeline
SKIP_DEFAULT = 0  # skips first n tweets for /timeline
LIMIT_DEFAULT = 10  # limits to n tweets for /timeline
LIMIT_OFFSET = 1  # offset for /timeline because redis is 0-indexed?
TTL = 60 * 60 * 24 * 7  # expire after n days

# tweet
CHARACTER_LIMIT = 280  # character limit for tweets

# search
#SEARCH_LIMIT_DEFAULT = 10  # limits to n tweets for /search
HASHTAGS_PER_SEARCH = 3  # limits to n hashtags for /search
USERS_PER_SEARCH = 5  # limits to n users for /search
