from PyQt5 import QtCore
from pathlib import Path
from widgets.imagewidget import ImageWidget
from widgets.imageswidget import ImagesWidget
from widgets.webpagewidget import WebPageWidget
from widgets.resourcewidget import ResourceWidget
from widgets.rsswidget import RssWidget
from tools.rssimages import RssImages
from tools.rssfeeds import RssFeeds
from tools.picklecache import PickleCache
from tools.urlimages import UrlImages


class Display():

    def __init__(self, centralWidget):
        self.centralWidget = centralWidget

    def start(self):
        cache_dir = Path.home() / '.cache/example'

        self._wallpaper = ImagesWidget(self.centralWidget, self._callback)
        self._wallpaper.imageprovider = UrlImages(
            cache_dir / 'Wallpaper',
            PickleCache(cache_dir / 'Wallpaper.pkl'))
        self._wallpaper.imageprovider.urls = ['https://papers.co/wallpaper/papers.co-mt01-winter-mountain-snow-bw-nature-white-35-3840x2160-4k-wallpaper.jpg']
        self._wallpaper.imagetimeout = 60000 # 1800000 # 30 minutes
        self._wallpaper.qrect = QtCore.QRect(0, 0, 1920, 1080)
        self._wallpaper.next = self._wallpaper
        self._wallpaper.start()

        self._rw = ResourceWidget(self.centralWidget, self._callback)
        self._rw.qrect = QtCore.QRect(800, 930, 320, 100)
        self._rw.start()

        self._lwpw1 = ImagesWidget(self.centralWidget, self._callback)
        self._lwpw1.imageprovider = RssImages(
            'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss',
            cache_dir / 'NasaImageOfTheDay',
            PickleCache(cache_dir / 'NasaImageOfTheDay.pkl'))
        self._lwpw1.imagetimeout = 11000
        self._lwpw1.background_visible = True
        self._lwpw1.text_visible = True
        self._lwpw1.bordersize = 4
        self._lwpw1.qrect = QtCore.QRect(15, 15, 800, 540)
        self._lwpw1.next = self._lwpw1
        self._lwpw1.start()

        self._rwpw1 = WebPageWidget(self.centralWidget, self._callback)
        self._rwpw1.url = 'https://www.python.org/'
        self._rwpw1.timeout = 60000
        self._rwpw1.qrect = QtCore.QRect(1105, 15, 800, 1050)

        feeds = RssFeeds(PickleCache(cache_dir / 'RssFeeds.pkl'))
        feeds.feed_urls = \
            ['http://rss.cnn.com/rss/edition.rss',
             'https://www.nu.nl/rss/Algemeen',
             'http://rss.slashdot.org/Slashdot/slashdotMain']
        feeds.limit_days = 31
        feeds.max_entries_per_feed = 3
        self._rwpw2 = RssWidget(self.centralWidget, self._callback)
        self._rwpw2.rss_entry_provider = feeds
        self._rwpw2.entrytimeout = 10000
        self._rwpw2.qrect = QtCore.QRect(1105, 15, 800, 1050)

        self._rwpw1.next = self._rwpw2
        self._rwpw2.next = self._rwpw1
        self._rwpw2.start()

    def _callback(self, widget):
        widget.stop()
        widget.next.start()
