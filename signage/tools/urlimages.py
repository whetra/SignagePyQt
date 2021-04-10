import wget
import urllib
from pathlib import Path
import imghdr
from datetime import timedelta
from datetime import datetime


class UrlImages():

    def __init__(self, images_directory: Path, cache):
        self._create_images_directory(images_directory)
        self.cache = cache
        self.cache_ttl = timedelta(days=1)
        self.urls = []

    def _create_images_directory(self, images_directory: Path):
        self.images_directory = images_directory
        if not self.images_directory.exists():
            self.images_directory.mkdir(parents=True)

    def getimages(self):
        for url in self.urls:
            filepath = self.getimage(url)
            if filepath is not None:
                yield filepath, ""

    def getimage(self, url):
        cache_item = self.cache.get(url)
        if self._is_valid_cache_item(cache_item, True):
            return str(cache_item.value)

        filepath = self._download_file(url)
        if self._is_valid_file(filepath):
            self.cache.set(url, filepath)
            return str(filepath)

        if self._is_valid_cache_item(cache_item, False):
            return str(cache_item.value)  # expired, but don't care
        return None

    def _is_valid_cache_item(self, cache_item, check_expired):
        if cache_item is None:
            return False
        elif check_expired and cache_item.is_expired(self.cache_ttl):
            return False
        return self._is_valid_file(cache_item.value)

    def _is_valid_file(self, filepath):
        if filepath is None:
            return False
        return filepath.exists()

    def _download_file(self, url):
        try:
            downloaded_filepath = wget.download(url, out=str(self.images_directory))
            image_type = imghdr.what(downloaded_filepath)
            if image_type is not None:
                p = Path(downloaded_filepath)
                new_filepath = Path(p.parent, "{}.{}".format(p.stem, image_type))
                p.rename(new_filepath)
                return new_filepath
            return None
        except urllib.error.URLError as e:
            print("{} UrlImages URLError {} ({})".format(datetime.now(), e, url))
            return None
        except urllib.error.HTTPError as e:
            print("{} UrlImages HTTPError {} ({})".format(datetime.now(), e, url))
            return None
        except FileNotFoundError as e:
            print("{} UrlImages FileNotFoundError {} ({}) ({})".format(datetime.now(), e, url, self.images_directory))
            return None
