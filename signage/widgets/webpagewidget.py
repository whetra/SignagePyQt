from PyQt5 import QtCore, QtWebKitWidgets
from .widgettimers import WidgetTimers


class WebPageWidget():

    def __init__(self, parentWidget, callback):
        self.parentWidget = parentWidget
        self.callback = callback
        self.url = ""
        self.timeout = 0
        self.qrect = QtCore.QRect(0, 0, 100, 100)
        self._timers = WidgetTimers(self._done, None, None)
        self._webEngineView1 = QtWebKitWidgets.QWebView(self.parentWidget)

    def start(self):
        self._webEngineView1.setGeometry(self.qrect)
        if self.timeout > 0:
            self._timers.start_timeout_timer(self.timeout)
        if self.url:
            self._webEngineView1.setHtml("")
            self._webEngineView1.setStyleSheet("background:transparent")
            self._webEngineView1.setUrl(QtCore.QUrl(self.url))
        self._webEngineView1.show()
        self._webEngineView1.raise_()

    def _done(self):
        self._timers.stop()
        self.callback(self)

    def stop(self):
        self._timers.stop()
        self._webEngineView1.setHtml("")
        self._webEngineView1.hide()
