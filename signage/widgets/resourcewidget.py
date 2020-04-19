from PyQt5 import QtCore, QtWidgets
import resource
from tools.timer import QTimerSingleShot


class ResourceWidget(QtCore.QObject):

    def __init__(self, parentWidget, callback):
        super().__init__()
        self.parentWidget = parentWidget
        self.callback = callback
        self.timeout = 0
        self.qrect = QtCore.QRect(0, 0, 100, 100)
        self._timeout_timer = QTimerSingleShot(self._done)
        self._label = QtWidgets.QLabel(self.parentWidget)
        self._text_timer = QTimerSingleShot(self._set_next_text)

    def start(self):
        self._label.setGeometry(self.qrect)
        self._label.setStyleSheet('background-color: white')
        self._set_next_text()
        self._label.show()
        self._label.raise_()

        if self.timeout > 0:
            self._timeout_timer.start(self.timeout)

    def _set_next_text(self):
        self._set_text()
        self._text_timer.start(2000)

    def _set_text(self):
        rusage = resource.getrusage(resource.RUSAGE_SELF)
        self._label.setText('ru_maxrss: {}'.format(rusage.ru_maxrss))

    def _done(self):
        self._timeout_timer.stop()
        self.callback(self)

    def stop(self):
        self._timeout_timer.stop()
        self._text_timer.stop()
        self._label.set_text('')
        self._label.hide()
