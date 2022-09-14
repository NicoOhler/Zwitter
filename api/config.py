REDIS_URL_FILE = "api/redis_url.key"  # file with redis url
REDIS_URL_FILE = "redis_url.key"  # file with redis url
with open(REDIS_URL_FILE) as file:  # read redis url from file
    REDIS_URL = file.read()

# timeline
SKIP_DEFAULT = 0  # skips first 0 tweets for /timeline
LIMIT_DEFAULT = 10  # limits to 10 tweets for /timeline
LIMIT_OFFSET = 1  # offset for /timeline because redis is 0-indexed?
TTL = 60 * 60 * 24 * 7  # expire after 7 days

CHARACTER_LIMIT = 280  # character limit for tweets