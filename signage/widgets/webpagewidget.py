from PyQt5 import QtCore, QtWebKitWidgets
from tools.timer import QTimerSingleShot


class WebPageWidget():

    def __init__(self, parentWidget, callback):
        self.parentWidget = parentWidget
        self.callback = callback
        self.url = ""
        self.timeout = 0
        self.qrect = QtCore.QRect(0, 0, 100, 100)
        self._timeout_timer = QTimerSingleShot(self._done)
        self._webEngineView1 = QtWebKitWidgets.QWebView(self.parentWidget)

    def start(self):
        self._webEngineView1.setGeometry(self.qrect)
        if self.timeout > 0:
            self._timeout_timer.start(self.timeout)
        if self.url:
            self._webEngineView1.setHtml("")
            self._webEngineView1.setStyleSheet("background:transparent")
            self._webEngineView1.setUrl(QtCore.QUrl(self.url))
        self._webEngineView1.show()
        self._webEngineView1.raise_()

    def _done(self):
        self._timeout_timer.stop()
        self.callback(self)

    def stop(self):
        self._timeout_timer.stop()
        self._webEngineView1.setHtml("")
        self._webEngineView1.hide()
