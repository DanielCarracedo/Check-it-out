import typing
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget,  QHeaderView, QTableWidgetItem, QApplication, QComboBox, QDateEdit, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QDate
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
            
            
        Controller.llenar_info(self)
        # Deshabilitar cambio de pagina por click en el QStackedWidget
        self.stackedWidget.setMouseTracking(False)

        # Cambio de pagina por los botones deseados
        self.Inicio.clicked.connect(self.go_to_page1)
        self.Home.clicked.connect(self.go_to_page1)
        self.Calendario.clicked.connect(self.go_to_page2)
        self.TareasPen.clicked.connect(self.go_to_page3)
        self.Crear.clicked.connect(self.go_to_page4)
        self.Settings.clicked.connect(self.go_to_page5)
        self.LogOut.clicked.connect(self.salir)

        # Otras funciones de los botones
        self.New.clicked.connect(self.create_task)
        self.adjustColumns(self.tableWidget)
        self.adjustColumns(self.tableWidget_2)
        Controller.llenar_tabla(self, True)
        self.tableWidget.itemClicked.connect(self.interactuar_tablas)
        self.tableWidget_2.itemClicked.connect(self.interactuar_tablas1)
        self.Oscuro.toggled.connect(self.invertir_colores)
        self.Noti.currentIndexChanged.connect(self.Cambio_Priori)
        #self.tableWidget.setColumnCount(7)
        self.resaltar_fecha_en_calendario()

        # Crear un hilo para ejecutar send_notification
        hilo = threading.Thread(target=self.ejecutar_notificacion)
        hilo.start()
        hilo_1 = threading.Thread(target=self.ejecutar_notificacion_1)
        hilo_1.start()
        
    def invertir_colores(self,checked):
        # Recorrer recursivamente los widgets y cambiar colores
        if checked:
            print(checked)
            #Guardamos los estilo que tienen los elementos a cambiar 
            Home=self.Home.styleSheet()
            Frame =self.frame_2.styleSheet()
            Edit= self.lineEdit.styleSheet()

            
            #Cambiamos los estilos a nuestracombeniencia
            self.centralwidget.setStyleSheet("background-color: black;")
            self.Home.setStyleSheet("color: white;")
            self.frame_2.setStyleSheet("QPushButton{border:none; color:white}")
            self.us.set_oscurodb()
        else:
            self.us.set_clarodb()
            pass

    def ejecutar_notificacion_1(self):
        Modelo.notifications.proximity_notification(self.us)

    def ejecutar_notificacion(self):
        # Llamar a la función send_notification en el hilo secundario
        Modelo.notifications.send_notification(self.us)
        
    def Cambio_Priori(self):
        self.us.set_priority(self.Noti.currentIndex())

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
        elif columna_clicada==6:
            for task in self.us.get_tasks():
                if task.get_ownid() == fila_clicada:
                    mensaje=f'¿Desea Eliminar esta tarea?'
                    respuesta = QMessageBox.question(self,'confirmacion',mensaje,QMessageBox.Yes|QMessageBox.No)
                    if respuesta == QMessageBox.Yes:
                        self.us.delete_task(task.get_ownid())
                        Controller.llenar_tabla(self,True)
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
        
    def go_to_page5(self):
        self.stackedWidget.setCurrentIndex(4)
        Controller.llenar_info(self)
        
    def salir(self):
        from UI.Login import Loginw
        
    def resaltar_fecha_en_calendario(self):
        for task in self.us.get_tasks():
            fecha = task.get_fecha_fin()
            fecha_a=QDate(fecha.year,fecha.month, fecha.day)
            # Establecer el formato del texto para resaltar la fecha
            formato_fecha_resaltada = self.calendarWidget.dateTextFormat(fecha_a)
            formato_fecha_resaltada.setBackground(Qt.gray)  # Cambia el color de fondo, por ejemplo, a verde
            # Aplicar el formato de texto a la fecha para resaltarla
            self.calendarWidget.setDateTextFormat(fecha_a, formato_fecha_resaltada)

    def create_task(self):
        ini = self.F_Inicio.dateTime()
        fin = self.F_Fin.dateTime()

        ini_f = ini.toPyDateTime()
        fin_f = fin.toPyDateTime()
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
