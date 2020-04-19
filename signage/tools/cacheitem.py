from datetime import datetime
from datetime import timedelta


class CacheItem:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.time = datetime.now()

    def is_expired(self, ttl: timedelta):
        if ttl is None:
            return False
        return datetime.now() > self.time + ttl
