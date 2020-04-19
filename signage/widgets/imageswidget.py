from PyQt5 import QtCore
from .image import Image
from tools.timer import QTimerSingleShot


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
        self._timeout_timer = QTimerSingleShot(self._done)
        self._image_timeout_timer = QTimerSingleShot(self._show_next_image)
        self._image = Image(self.parentWidget)

    def start(self):
        self._image.setGeometry(self.qrect)
        self._images = self.imageprovider.getimages() if self.imageprovider is not None else iter(())
        if self.timeout > 0:
            self._timeout_timer.start(self.timeout)
        self._show_next_image()
        self._image.show()
        self._image.raise_()

    def _show_next_image(self):
        try:
            image, title = next(self._images)
            self._show_image(image, title)
            self._image_timeout_timer.start(self.imagetimeout)
        except StopIteration:
            self._done()

    def _show_image(self, image, title):
        self._image.background_visible = self.background_visible
        self._image.text_visible = self.text_visible
        self._image.bordersize = self.bordersize
        self._image.set_image(image, title)

    def _done(self):
        self._image_timeout_timer.stop()
        self._timeout_timer.stop()
        self.callback(self)

    def stop(self):
        self._image_timeout_timer.stop()
        self._timeout_timer.stop()
        self._image.hide()
