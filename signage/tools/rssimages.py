from pathlib import Path
from .urlimages import UrlImages
from .rssfeeds import RssFeeds


class RssImages():

    def __init__(self, feed_url, images_directory: Path, cache):
        self.feeds = RssFeeds(cache)
        self.feeds.feed_urls = [feed_url]
        self.imageprovider = UrlImages(images_directory, cache)

    def getimages(self):
        entries = self.feeds.get_entries()
        entries = sorted(entries, key=lambda entry: entry.published_datetime)  # undo reversed sort
        for entry in entries:
            if entry.image:
                filepath = self.imageprovider.getimage(entry.image)
                if filepath is not None:
                    yield filepath, entry.title
