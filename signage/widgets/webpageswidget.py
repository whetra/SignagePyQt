from PyQt5 import QtCore, QtWebKitWidgets, QtWidgets
from .widgettimers import WidgetTimers


class WebPagesWidget():

    def __init__(self, parentWidget, callback):
        self.parentWidget = parentWidget
        self.callback = callback
        self.url_provider = None
        self.timeout = 0
        self.url_timeout = 10000  # milliseconds
        self.qrect = QtCore.QRect(0, 0, 100, 100)
        self.animate = True
        self.animation = None
        self._timers = WidgetTimers(self._done, self._show_next_url, self._done)
        self._parent = QtWidgets.QWidget(self.parentWidget)
        self._parent.hide()
        self._webEngineView1 = QtWebKitWidgets.QWebView(self._parent)
        self._webEngineView1.setStyleSheet("background: transparent")
        self._webEngineView1.setHtml("")  # prevents blurry background
        self._done_timeout = 2000  # wait 2 seconds when no entries were shown to prevent high cpu usage

    def start(self):
        self._urls = self.url_provider.get_urls() if self.url_provider is not None else iter(())
        if self.timeout > 0:
            self._timers.start_timeout_timer(self.timeout)
        self._done_timeout = 2000  # reset _done_timeout
        self._show_next_url()
        self._parent.show()
        self._parent.raise_()

    def _show_next_url(self):
        try:
            nexturl = next(self._urls)
            self._done_timeout = 100  # wait 100 ms
            self._set_url(nexturl)
            self._timers.start_next_timer(self.url_timeout)
        except StopIteration:
            self._timers.start_done_timer(self._done_timeout)

    def _set_url(self, nexturl):
        if self.animate:
            self._animate_geometry()
        else:
            self._parent.setGeometry(self.qrect)
        self._webEngineView1.setGeometry(QtCore.QRect(0, 0, self.qrect.width(), self.qrect.height()))
        self._webEngineView1.setHtml("")
        self._webEngineView1.setStyleSheet("background:transparent;")
        self._webEngineView1.setUrl(QtCore.QUrl(nexturl))

    def _animate_geometry(self):
        if self.animation is None:
            self.animation = QtCore.QPropertyAnimation(self._parent, b"geometry")
            self.animation.setDuration(400)
        self.animation.setStartValue(QtCore.QRect(self.qrect.left() + self.qrect.width() / 2, self.qrect.top(), 0, self.qrect.height()))
        self.animation.setEndValue(self.qrect)
        self.animation.start()

    def _done(self):
        self._timers.stop()
        self.callback(self)

    def stop(self):
        self._timers.stop()
        self._webEngineView1.setHtml("")
        self._parent.hide()
