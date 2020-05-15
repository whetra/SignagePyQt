from PyQt5 import QtCore, QtWebKitWidgets, QtWidgets
from tools.timer import QTimerSingleShot


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
        self._timeout_timer = QTimerSingleShot(self._done)
        self._url_timeout_timer = QTimerSingleShot(self._show_next_url)
        self._parent = QtWidgets.QWidget(self.parentWidget)
        self._parent.hide()
        self._webEngineView1 = QtWebKitWidgets.QWebView(self._parent)

    def start(self):
        self._urls = self.url_provider.get_urls() if self.url_provider is not None else iter(())
        if self.timeout > 0:
            self._timeout_timer.start(self.timeout)
        self._show_next_url()
        self._parent.show()
        self._parent.raise_()

    def _show_next_url(self):
        try:
            nexturl = next(self._urls)
            self._set_url(nexturl)
            self._url_timeout_timer.start(self.url_timeout)
        except StopIteration:
            self._done()

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
        self._url_timeout_timer.stop()
        self._timeout_timer.stop()
        self.callback(self)

    def stop(self):
        self._url_timeout_timer.stop()
        self._timeout_timer.stop()
        self._webEngineView1.setHtml("")
        self._parent.hide()
