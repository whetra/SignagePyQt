import feedparser
from datetime import datetime
from datetime import timedelta
from urllib.parse import urlparse


class RssEntry:

    def __init__(self):
        self.title = ''
        self.description = ''
        self.published_datetime = datetime.now()
        self.link = ''
        self.short_link = ''
        self.image = ''
        self.enclosures = []


class RssFeeds:

    def __init__(self, cache):
        self.cache = cache
        self.cache_ttl = timedelta(minutes=30)
        self.feed_urls = []
        self.limit_days = None  # None = no limit
        self.max_entries_per_feed = None  # None = all entries

    def get_entries(self):
        for feed_url in self.feed_urls:
            feed = self._parse_feed(feed_url)
            if feed is not None:
                for entry in self._mapfiltersort_entries(feed.entries):
                    yield entry

    def _parse_feed(self, feed_url):
        cache_item = self.cache.get(feed_url)
        if self._is_valid_cache_item(cache_item, True):
            return cache_item.value

        feed = feedparser.parse(feed_url)
        if self._is_valid_feed(feed_url, feed):
            self.cache.set(feed_url, feed)
            return feed

        if self._is_valid_cache_item(cache_item, False):
            return cache_item.value  # expired, but don't care
        return None

    def _is_valid_cache_item(self, cache_item, check_expired):
        if cache_item is None:
            return False
        elif check_expired and cache_item.is_expired(self.cache_ttl):
            return False
        return self._is_valid_feed(cache_item.key, cache_item.value)

    def _is_valid_feed(self, feed_url, feed):
        if feed is None:
            return False
        elif 'bozo_exception' in feed:
            print(f'{datetime.now()} {feed_url}: {feed.bozo_exception}')
            return False
        return True

    def _mapfiltersort_entries(self, entries):
        min_date = datetime.now() - timedelta(self.limit_days) if self.limit_days is not None else datetime.min
        rss_entries = list(map(lambda entry: self._create_rssentry(entry), entries))
        rss_entries = list(filter(lambda entry: entry.published_datetime > min_date, rss_entries))
        rss_entries = sorted(rss_entries, key=lambda entry: entry.published_datetime, reverse=True)
        rss_entries = rss_entries[:self.max_entries_per_feed]
        return rss_entries

    def _create_rssentry(self, entry):
        re = RssEntry()
        re.title = self._get_title(entry)
        re.description = self._get_description(entry)
        re.published_datetime = self._get_published_datetime(entry)
        re.link = entry.link
        re.short_link = self._get_short_link(entry)
        re.image = self._get_image(entry)
        return re

    def _get_title(self, entry):
        if 'title' not in entry:
            return ''
        return entry.title

    def _get_description(self, entry):
        if 'description' not in entry:
            return ''
        return entry.description

    def _get_image(self, entry):
        for enclosure in entry.enclosures:
            if enclosure.type.startswith('image/'):
                return enclosure.href
        return ''

    def _get_published_datetime(self, entry):
        # published_parsed returns standard Python 9-tuple
        # when constructing datetime we need year to seconds (6 fields)
        if 'published' in entry:
            return datetime(*entry.published_parsed[:6])
        if 'updated' in entry:
            return datetime(*entry.updated_parsed[:6])
        return datetime.min  # cannot be None, because we want to sort

    def _get_short_link(self, entry):
        o = urlparse(entry.link)
        if o.netloc:
            server = o.netloc.split(':', 1)[0]
            return f'{o.scheme}://{server}'
        elif o.path:
            server = o.path.split('/', 1)[0]
            return f'{o.scheme}://{server}'
        return ''
