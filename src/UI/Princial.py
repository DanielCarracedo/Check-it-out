import typing
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget,  QHeaderView, QTableWidgetItem,QApplication, QComboBox, QDateEdit, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5 import QtCore, QtWidgets, uic
import sys
import pickle
import datetime
from copy import deepcopy
import threading
import Modelo.notifications

class PrincipalWg(QMainWindow):
    def __init__(self) -> None:
        super(PrincipalWg,self).__init__()
        uic.loadUi("Check_it_out.ui",self)
        self.click_posicion = None
        self.showMaximized()
        self.page =None
        from Modelo.User import User

        with open('usuario.pkl', 'rb') as archivo:
            self.us = pickle.load(archivo)
        
        #Deshabilitar cambio de pagina por click en el QStackedWidget
        self.stackedWidget.setMouseTracking(False)
        
        #Cambio de pagina por los botones deseados
        self.Inicio.clicked.connect(self.go_to_page1)
        self.Calendario.clicked.connect(self.go_to_page2)
        self.TareasPen.clicked.connect(self.go_to_page3)
        self.Crear.clicked.connect(self.go_to_page4)
        
        # Otras funciones de los botones
        self.New.clicked.connect(self.create_task)
        self.adjustColumns(self.tableWidget)
        self.adjustColumns(self.tableWidget_2)
        self.populateTable()
        self.tableWidget.itemClicked.connect(self.mostrar_informacion)
        
        # Crear un hilo para ejecutar send_notification
        hilo = threading.Thread(target=self.ejecutar_notificacion)
        hilo.start()
        hilo_1 =threading.Thread(target=self.ejecutar_notificacion_1)
        hilo_1.start()
    def ejecutar_notificacion_1(self):
        Modelo.notifications.proximity_notification(self.us)

    def ejecutar_notificacion(self):
        # Llamar a la función send_notification en el hilo secundario
        Modelo.notifications.send_notification(self.us)
    
        
    def mostrar_informacion(self, item):
        # Obtener el texto del elemento clicado
        texto = item.text()

        # Mostrar un cuadro de diálogo de información
        QMessageBox.information(self, 'Información', f'{texto}')
        
    def adjustColumns(self, table):
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
    def populateTable(self):
        data = []
        for task in self.us.get_tasks():
            if task.get_finished() == True:
                est = "Completado"
            else:
                est = "No completado"
            info = [
                f'{task.get_titulo()}',  # Columna para el título
                f'{task.get_categoria()}',
                f'{task.get_fecha_in()}',
                f'{task.get_desc()}',
                f'{task.get_fecha_fin()}',
                f'{est}'  # Columna para el estado (Completado/No completado)
            ]
            data.append(deepcopy(info))  # Usar deepcopy para agregar una copia de 'info' a 'data'
        print(data)
    
        # Establecer el número de filas y columnas en la tabla
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0])) if data else 0

        # Llenar la tabla con los datos
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.tableWidget.setItem(i, j, item)
                
    def FilTable(self):
        data = []
    
        for task in self.us.get_tasks():
            if task.get_finished() == False:
                print("aqui toy")
                est = "No completado"
                info = [
                f'{task.get_titulo()}',  # Columna para el título
                f'{task.get_categoria()}',
                f'{task.get_fecha_in()}',
                f'{task.get_desc()}',
                f'{task.get_fecha_fin()}',
                f'{est}'  # Columna para el estado (Completado/No completado)
                ]
                data.append(deepcopy(info))  # Usar deepcopy para agregar una copia de 'info' a 'data'
    
        # Establecer el número de filas y columnas en la tabla
        self.tableWidget_2.setRowCount(len(data))
        self.tableWidget_2.setColumnCount(len(data[0])) if data else 0

        # Llenar la tabla con los datos
        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                self.tableWidget_2.setItem(i, j, item)
                
    def go_to_page1(self):
        self.stackedWidget.setCurrentIndex(0)
        self.populateTable()
        

    def go_to_page2(self):
        self.stackedWidget.setCurrentIndex(1)


    def go_to_page3(self):
        self.stackedWidget.setCurrentIndex(2)
        self.FilTable()
        
    def go_to_page4(self):
        self.stackedWidget.setCurrentIndex(3)

        
    def create_task(self):
        from Controler import Controller
        con = Controller()
        print(type(self.us))
        print(self.us.get_Name())
        ini=self.F_Inicio.date()
        fin=self.F_Fin.date()
        ini_f = datetime.datetime(ini.year(), ini.month(), ini.day())
        fin_f = datetime.datetime(fin.year(), fin.month(), fin.day())
        #Creacion de la tarea
        con.new_task(self.us, self.Tipo.currentText(),ini_f ,fin_f,self.Descripcion.text(),self.Tarea_Name.text())
        #Limpiar los elementos donde se crearon la tarea
        self.Tipo.setCurrentIndex(-1)  # Desmarcar cualquier selección
        self.F_Inicio.setDate(self.F_Inicio.minimumDate())  # Establecer la fecha mínima o limpia
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
