import typing
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget,  QHeaderView, QTableWidgetItem, QApplication, QComboBox, QDateEdit, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5 import QtCore, QtWidgets, uic
import sys
import pickle
import datetime
from copy import deepcopy
import threading
import Modelo.notifications
from Controler import Controller


class PrincipalWg(QMainWindow):
    def __init__(self) -> None:
        super(PrincipalWg, self).__init__()
        uic.loadUi("Check_it_out.ui", self)
        self.click_posicion = None
        self.showMaximized()
        self.page = None
        from Modelo.User import User

        with open('usuario.pkl', 'rb') as archivo:
            self.us = pickle.load(archivo)

        # Deshabilitar cambio de pagina por click en el QStackedWidget
        self.stackedWidget.setMouseTracking(False)

        # Cambio de pagina por los botones deseados
        self.Inicio.clicked.connect(self.go_to_page1)
        self.Calendario.clicked.connect(self.go_to_page2)
        self.TareasPen.clicked.connect(self.go_to_page3)
        self.Crear.clicked.connect(self.go_to_page4)

        # Otras funciones de los botones
        self.New.clicked.connect(self.create_task)
        self.adjustColumns(self.tableWidget)
        self.adjustColumns(self.tableWidget_2)
        Controller.llenar_tabla(self, True)
        self.tableWidget.itemClicked.connect(self.interactuar_tablas)
        self.tableWidget_2.itemClicked.connect(self.interactuar_tablas1)

        # Crear un hilo para ejecutar send_notification
        hilo = threading.Thread(target=self.ejecutar_notificacion)
        hilo.start()
        hilo_1 = threading.Thread(target=self.ejecutar_notificacion_1)
        hilo_1.start()

    def ejecutar_notificacion_1(self):
        Modelo.notifications.proximity_notification(self.us)

    def ejecutar_notificacion(self):
        # Llamar a la función send_notification en el hilo secundario
        Modelo.notifications.send_notification(self.us)

    def interactuar_tablas(self, item):
        columna_clicada = item.column()
        fila_clicada = item.row()
        # Realizar la acción correspondiente según la columna
        if columna_clicada == 5:
            for task in self.us.get_tasks():
                if task.get_ownid() == fila_clicada:
                    if item.text() == "No completado":
                        mensaje = f"¿Seguro que deseas marcar la Tarea #{fila_clicada + 1} como completa?"
                        respuesta = QMessageBox.question(
                            self, 'Confirmación', mensaje, QMessageBox.Yes | QMessageBox.No)
                        if respuesta == QMessageBox.Yes:
                            task.set_completed()
                    else:
                        mensaje = f"¿Seguro que deseas marcar la Tarea #{fila_clicada + 1} como No completa?"
                        respuesta = QMessageBox.question(
                            self, 'Confirmación', mensaje, QMessageBox.Yes | QMessageBox.No)
                        if respuesta == QMessageBox.Yes:
                            task.set_uncompleted()
            Controller.llenar_tabla(self, True)
        else:
            # Obtener el texto del elemento clicado
            texto = item.text()
        # Mostrar un cuadro de diálogo de información
            QMessageBox.information(self, 'Información', f'{texto}')

    def interactuar_tablas1(self, item):
        texto = item.text()
        # Mostrar un cuadro de diálogo de información
        QMessageBox.information(self, 'Información', f'{texto}')

    def adjustColumns(self, table):
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def go_to_page1(self):
        self.stackedWidget.setCurrentIndex(0)
        Controller.llenar_tabla(self, True)

    def go_to_page2(self):
        self.stackedWidget.setCurrentIndex(1)

    def go_to_page3(self):
        self.stackedWidget.setCurrentIndex(2)
        Controller.llenar_tabla(self, False)

    def go_to_page4(self):
        self.stackedWidget.setCurrentIndex(3)

    def create_task(self):
        ini = self.F_Inicio.date()
        fin = self.F_Fin.date()
        ini_f = datetime.datetime(ini.year(), ini.month(), ini.day())
        fin_f = datetime.datetime(fin.year(), fin.month(), fin.day())
        # Creacion de la tarea
        Controller.new_task(self.us, self.Tipo.currentText(
        ), ini_f, fin_f, self.Descripcion.text(), self.Tarea_Name.text())
        # Limpiar los elementos donde se crearon la tarea
        self.Tipo.setCurrentIndex(-1)  # Desmarcar cualquier selección
        # Establecer la fecha mínima o limpia
        self.F_Inicio.setDate(self.F_Inicio.minimumDate())
        self.F_Fin.setDate(self.F_Fin.minimumDate())
        self.Descripcion.clear()
        self.Tarea_Name.clear()
        self.go_to_page1()

    def entrar(self):
        if __name__ == '__main__':
            app = QApplication([])
            window = PrincipalWg()
            window.show()
            app.exec_()
