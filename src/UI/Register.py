from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5 import QtCore, QtWidgets, uic
import sys

class Register(QMainWindow):
    def __init__(self):
        super(Register, self).__init__()
        uic.loadUi("Register.ui",self)
        self.Bt_normal.hide()
        self.click_posicion = None
        self.Bt_min.clicked.connect(self.showMinimized)
        self.Bt_normal.clicked.connect(self.control_bt_normal)
        self.Bt_max.clicked.connect(self.control_bt_maximize)
        self.Bt_close.clicked.connect(self.close)

        # Eliminar títulos y opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

    def control_bt_normal(self):
        self.showNormal()
        self.Bt_normal.hide()
        self.Bt_max.show()

    def control_bt_maximize(self):
        self.showMaximized()
        self.Bt_max.hide()
        self.Bt_normal.show()

    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    def mousePressEvent(self, event):
        self.click_posicion = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.click_posicion)
                self.click_posicion = event.globalPos()
                event.accept()

        if event.globalPos().y() <= 5 or event.globalPos().x() <= 5:
            self.showMaximized()
            self.Bt_max.hide()
            self.Bt_normal.show()
        else:
            self.showNormal()
            self.Bt_normal.hide()
            self.Bt_max.show()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = Register()
    my_app.show()
    sys.exit(app.exec_())