from pathlib import Path
import pickle
from datetime import timedelta
from datetime import datetime
from .cacheitem import CacheItem


class PickleCache:

    def __init__(self, pickle_file: Path):
        self.pickle_file = pickle_file
        if not self.pickle_file.parent.exists():
            self.pickle_file.parent.mkdir(parents=True)

    def del_expired(self, ttl: timedelta):
        cache = self._read_cache()
        for k in list(cache.keys()):
            if cache[k].is_expired(ttl):
                del cache[k]

    def get(self, key):
        cache = self._read_cache()
        if key in cache:
            return cache[key]
        return None

    def set(self, key, value):
        # for now read and write cache with every set
        cache = self._read_cache()
        cache[key] = CacheItem(key, value)
        self._write_cache(cache)

    def _write_cache(self, cache):
        with self.pickle_file.open("wb") as f:
            pickle.dump(cache, f)

    def _read_cache(self):
        if not self.pickle_file.exists():
            return {}
        try:
            with self.pickle_file.open("rb") as f:
                return pickle.loads(f.read())
        except EOFError as e:
            print("{} PickleCache {} EOFError: {}".format(datetime.now(), self.pickle_file, e))
            return {}
        except Exception as e:
            print("{} PickleCache {} Exception: {}".format(datetime.now(), self.pickle_file, e))
            return {}
