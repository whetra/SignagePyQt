from PyQt5 import QtCore, QtGui, QtWidgets


class Image(QtWidgets.QWidget):

    def __init__(self, parentWidget):
        super().__init__(parentWidget)
        self._backgroundframe = QtWidgets.QFrame(self)
        self._backgroundframe.setStyleSheet('background-color: rgba(0, 0, 0, 0.6); border-radius: 8px;')
        self._backgroundframe.hide()
        self._imagelabel = QtWidgets.QLabel(self)
        self._imagelabel.hide()
        self._textlabel = QtWidgets.QLabel(self)
        self._textlabel.setStyleSheet('font-family: Arial, Helvetica, sans-serif; font-size: 24px; color: #FFFFFF')
        self._textlabel.hide()

        self.background_visible = False
        self.text_visible = False
        self.bordersize = 0

    def set_image(self, image_file, text=''):
        textheightadjustment = self._textlabel.height() if self.text_visible else 0
        max_imagesize = self.geometry().adjusted(self.bordersize, self.bordersize, -self.bordersize, -self.bordersize - textheightadjustment)
        pixmap = QtGui.QPixmap(image_file)
        if pixmap and not pixmap.isNull():
            pixmap = pixmap.scaled(max_imagesize.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self._imagelabel.setPixmap(pixmap)
            self._imagelabel.show()
            pixmap_rect = pixmap.rect()
        else:
            print('pixmap.isNull(): ' + image_file)
            self._imagelabel.hide()  # hide image, but still show background and text if applicable
            pixmap_rect = self._imagelabel.rect()  # keep current size
        self._backgroundframe.show() if self.background_visible else self._backgroundframe.hide()
        self._textlabel.setText(text)
        self._textlabel.show() if self.text_visible else self._textlabel.hide()
        self._position_widgets(pixmap_rect)

    def _position_widgets(self, pixmap_rect):
        textheightadjustment = self._textlabel.height() if self.text_visible else 0
        image_rect = pixmap_rect.translated(self.bordersize, self.bordersize)
        background_rect = image_rect.adjusted(-self.bordersize, -self.bordersize, self.bordersize, self.bordersize + textheightadjustment)
        text_rect = QtCore.QRect(image_rect.left(), image_rect.bottom() + 1, image_rect.width(), textheightadjustment)

        centeroffset = int((self.geometry().width() - background_rect.width()) / 2)
        image_rect.translate(centeroffset, 0)
        background_rect.translate(centeroffset, 0)
        text_rect.translate(centeroffset, 0)

        self._backgroundframe.setGeometry(background_rect)
        self._imagelabel.setGeometry(image_rect)
        self._textlabel.setGeometry(text_rect)
