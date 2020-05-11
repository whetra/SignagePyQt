from PyQt5 import QtCore, QtWidgets
import os
import psutil
from datetime import datetime
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
        text = self._get_text()
        self._label.setWordWrap(True)
        self._label.setText(text)

    def _get_text(self):
        pid = os.getpid()
        proc = psutil.Process(pid)
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        started = datetime.fromtimestamp(proc.create_time()).strftime('%Y-%m-%d %H:%M:%S')
        mem = psutil.virtual_memory()
        proc_mem = proc.memory_info()
        io_counters = proc.io_counters()
        return (
            f"boot: {boot_time}\n"
            f"started: {started}\n"
            f"memory: total={self.bytes2human(mem.total)}, used={self.bytes2human(mem.used)}\n"
            f"process memory: {self.bytes2human(proc_mem.rss)}\n"
            f"process io: read_count={self.bytes2human(io_counters.read_count)}, write_count={self.bytes2human(io_counters.write_count)}\n"
            f"            read_bytes={self.bytes2human(io_counters.read_bytes)}, write_bytes={self.bytes2human(io_counters.write_bytes)}\n"
        )

    def bytes2human(self, n, format="%(value).1f%(symbol)s"):
        symbols = ('B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols[1:]):
            prefix[s] = 1 << (i + 1) * 10
        for symbol in reversed(symbols[1:]):
            if n >= prefix[symbol]:
                value = float(n) / prefix[symbol]
                return format % locals()
        return format % dict(symbol=symbols[0], value=n)

    def _done(self):
        self._timeout_timer.stop()
        self.callback(self)

    def stop(self):
        self._timeout_timer.stop()
        self._text_timer.stop()
        self._label.set_text('')
        self._label.hide()
