import typing
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QWidget
from PyQt5 import QtCore, QtWidgets, uic
from UI.Login import Loginw
import sys

l =Loginw()

class PrincipalWg(QMainWindow):
    def __init__(self) -> None:
        super(PrincipalWg,self).__init__()
        uic.loadUi("Check_it_out.ui",self)
        self.click_posicion = None
        self.showMaximized()
        self.Log = l.User
        
        
        #Deshabilitar cambio de pagina por click en el QStackedWidget
        self.stackedWidget.setMouseTracking(False)
        
        #Cambio de pagina por los botones deseados
        self.Inicio.clicked.connect(self.go_to_page1)
        self.Calendario.clicked.connect(self.go_to_page2)
        self.TareasPen.clicked.connect(self.go_to_page3)
        
    def go_to_page1(self):
        self.stackedWidget.setCurrentIndex(0)

    def go_to_page2(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_page3(self):
        self.stackedWidget.setCurrentIndex(2)

    def entrar(self):
        if __name__ == '__main__':
            app = QApplication([])
            window = PrincipalWg()
            window.show()
            app.exec_()
