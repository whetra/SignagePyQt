from PyQt5 import QtCore


class WidgetTimers:

    def __init__(self, timeout_callback, next_callback, done_callback):
        self._timeout_timer = QtCore.QTimer()
        self._timeout_timer.setSingleShot(True)
        if timeout_callback:
            self._timeout_timer.timeout.connect(timeout_callback)

        self._next_timer = QtCore.QTimer()
        self._next_timer.setSingleShot(True)
        if next_callback:
            self._next_timer.timeout.connect(next_callback)

        self._done_timer = QtCore.QTimer()
        self._done_timer.setSingleShot(True)
        if done_callback:
            self._done_timer.timeout.connect(done_callback)

    def start_timeout_timer(self, timeout):
        self._timeout_timer.start(timeout)

    def start_next_timer(self, timeout):
        self._next_timer.start(timeout)

    def start_done_timer(self, timeout):
        self._done_timer.start(timeout)

    def stop(self):
        self._next_timer.stop()
        self._timeout_timer.stop()
        self._done_timer.stop()
