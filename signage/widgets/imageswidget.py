from PyQt5 import QtCore
from .image import Image
from .widgettimers import WidgetTimers


class ImagesWidget():

    def __init__(self, parentWidget, callback):
        self.parentWidget = parentWidget
        self.callback = callback
        self.imageprovider = None
        self.timeout = 0
        self.imagetimeout = 10000  # milliseconds
        self.background_visible = False
        self.text_visible = False
        self.bordersize = 0
        self.qrect = QtCore.QRect(0, 0, 100, 100)
        self._timers = WidgetTimers(self._done, self._show_next_image, self._done)
        self._image = Image(self.parentWidget)
        self._done_timeout = 2000  # wait 2 seconds when no entries were shown to prevent high cpu usage

    def start(self):
        self._image.setGeometry(self.qrect)
        self._images = self.imageprovider.getimages() if self.imageprovider is not None else iter(())
        if self.timeout > 0:
            self._timers.start_timeout_timer(self.timeout)
        self._done_timeout = 2000  # reset _done_timeout
        self._show_next_image()
        self._image.show()

    def _show_next_image(self):
        try:
            image, title = next(self._images)
            self._show_image(image, title)
            self._done_timeout = 100  # wait 100 ms
            self._timers.start_next_timer(self.imagetimeout)
        except StopIteration:
            self._timers.start_done_timer(self._done_timeout)

    def _show_image(self, image, title):
        self._image.background_visible = self.background_visible
        self._image.text_visible = self.text_visible
        self._image.bordersize = self.bordersize
        self._image.set_image(image, title)

    def _done(self):
        self._timers.stop()
        self.callback(self)

    def stop(self):
        self._timers.stop()
        self._image.hide()
