from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QTimer
from Controler import Controller
from Modelo.sist import Chekitout
import time
import sys
import pickle


global usuario


class Loginw(QMainWindow):
    def __init__(self):
        super(Loginw, self).__init__()
        uic.loadUi("Log.ui", self)
        self.Bt_normal.hide()
        self.click_posicion = None
        self.Bt_min.clicked.connect(self.showMinimized)
        self.Reg.clicked.connect(self.GuiRegister)
        self.Bt_normal.clicked.connect(self.control_bt_normal)
        self.Bt_max.clicked.connect(self.control_bt_maximize)
        self.Bt_close.clicked.connect(self.close)
        self.Enter.clicked.connect(self.Confirm)

        # Eliminar títulos y opacidad
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

    def GuiRegister(self):
        from UI.Register import Register
        self.hide()
        self.register_window = Register()  # Crear una instancia de Register
        self.register_window.show()  # Mostrar la ventana de registro

    def Confirm(self) -> "User":
        u=self.User.text(); p=self.Password.text()
        if not u.strip() or not p.strip():
            self.Mensaje.setText("Error!, hay espacios en blanco por favor, \n llene la informacion requerida.")
            QTimer.singleShot(4000, lambda: self.Mensaje.setText(""))
        else: 
            x = Controller.confirm_user(
            self, self.User.text(), self.Password.text())
        

    def Prin(self):
        from UI.Princial import PrincipalWg
        self.prin = PrincipalWg()
        self.hide()
        self.prin.entrar()

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
        self.grip.move(rect.right() - self.gripSize,
                       rect.bottom() - self.gripSize)

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
    
    def volver():
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            my_app = Loginw()
            my_app.show()
            app.exec_()
