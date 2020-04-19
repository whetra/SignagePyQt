from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import getopt  # Only needed for access to command line arguments
import importlib
from importlib.machinery import SourceFileLoader


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Signage")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint or QtCore.Qt.CustomizeWindowHint)
        self.showFullScreen()
        self.setCentralWidget(QtWidgets.QWidget(self))

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self)
        shortcut.activated.connect(lambda: QtWidgets.QApplication.quit())

    def show(self):
        super().show()
        self._display = self._get_display()
        self._display.start()

    def _get_display(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'n:p:u:', ['display_name=', 'display_path=', 'display_url='])
        except getopt.GetoptError:
            print('Unknown arguments')
            sys.exit(2)

        try:
            for opt, arg in opts:
                if opt in ("-n", "--display_name"):
                    return self._get_display_by_name(arg)
                elif opt in ("-p", "--display_path"):
                    return self._get_display_from_path(arg)
                elif opt in ("-u", "--display_url"):
                    return self._get_display_from_url(arg)
            return self._get_default_display()
        except Exception as e:
            print('Error getting Display: ' + str(e))
            sys.exit(2)

    def _get_default_display(self):
        return self._get_display_by_name('default')

    def _get_display_by_name(self, display_name):
        mod = importlib.import_module('displays.' + display_name)
        return mod.Display(self.centralWidget())

    def _get_display_from_path(self, display_path):
        display_module = SourceFileLoader('Display', display_path).load_module()
        display_class = getattr(display_module, 'Display')
        display = display_class(self.centralWidget())
        return display

    def _get_display_from_url(self, display_url):
        print('Display from URL not supported yet')
        sys.exit(2)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
