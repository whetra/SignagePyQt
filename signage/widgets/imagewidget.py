from PyQt5 import QtCore, QtWebKitWidgets
from .widgettimers import WidgetTimers


class ImageWidget():

    def __init__(self, parentWidget, callback):
        self.parentWidget = parentWidget
        self.callback = callback
        self.image = ""
        self.timeout = 0
        self.qrect = QtCore.QRect(0, 0, 100, 100)
        self._timers = WidgetTimers(self._done, None, None)
        self._webEngineView1 = QtWebKitWidgets.QWebView(self.parentWidget)

    def start(self):
        self._webEngineView1.setGeometry(self.qrect)
        if self.image:
            self._webEngineView1.setHtml("")  # crash if not emptied first
            self._webEngineView1.setUrl(QtCore.QUrl(self.image))
            self._webEngineView1.setStyleSheet("background:transparent")
        self._webEngineView1.show()

        if self.timeout > 0:
            self._timers.start_timeout_timer(self.timeout)

    def _done(self):
        self._timers.stop()
        self.callback(self)

    def stop(self):
        self._timers.stop()
        self._webEngineView1.setHtml("")
        self._webEngineView1.hide()
