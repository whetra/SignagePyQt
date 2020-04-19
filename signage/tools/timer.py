from PyQt5 import QtCore


class QTimerSingleShot(QtCore.QTimer):

    def __init__(self, callback):
        super().__init__()
        self.setSingleShot(True)
        self.timeout.connect(callback)
