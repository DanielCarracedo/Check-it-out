from Modelo.Task import Task
from PyQt5.QtWidgets import QTableWidgetItem
from Modelo.sist import Chekitout
from Modelo.User import User
from copy import deepcopy
from PyQt5.QtCore import QTimer
import datetime as dt
import pickle


class Controller():

    def Register(self, window, name: str, lastname: str, username: str, psw: str):
        sis = Chekitout()
        x = sis.register_user(name, lastname, username, psw)
        # Falta poner el mensajito en la pantalla register
        if x == True:
            return True
        elif x == False:
             window.confirm.setText("Error, usuario ya existente")
             QTimer.singleShot(4000, lambda: window.confirm.setText(""))
        elif x == 4:
             window.confirm.setText("Error!, el servidor esta presentando problemas, intente mas tarde!")
             QTimer.singleShot(4000, lambda: window.confirm.setText(""))

    def confirm_user(window, username: str, psw: str) -> bool:
        sis = Chekitout()
        x = sis.check_user(username, psw)
        if x == True:
            usuario = sis.create_session(window.User.text())
            with open('usuario.pkl', 'wb') as archivo:
                pickle.dump(usuario, archivo)
            window.Prin()

        elif x == False:
            window.Mensaje.setText(
                "Error! Usuario y/o contraseña incorrecta,\nverifique nuevamente")
            QTimer.singleShot(4000, lambda: window.Mensaje.setText(""))

        elif x == 4:
            window.Mensaje.setText(
                "Error! El servidor presenta problemas\nintente más tarde")
            QTimer.singleShot(4000, lambda: window.Mensaje.setText(""))

    def new_task(user: "User", categoria: str, fecha_in: dt, fecha_fin: dt, desc: str, titulo: str) -> bool:
        X = user.create_task(categoria, fecha_in, fecha_fin, desc, titulo)


    def llenar_tabla(window, page):
        data = []
        if page:
            for task in window.us.get_tasks():
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
                    # Columna para el estado (Completado/No completado)
                    f'{est}',
                    f' '
                ]
                # Usar deepcopy para agregar una copia de 'info' a 'data'
                data.append(deepcopy(info))

            # Establecer el número de filas y columnas en la tabla
            window.tableWidget.setRowCount(len(data))
            window.tableWidget.setColumnCount(len(data[0])) if data else 0

            # Llenar la tabla con los datos
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(col)
                    window.tableWidget.setItem(i, j, item)
        else:
            for task in window.us.get_tasks():
                if task.get_finished() == False:
                    est = "No completado"
                    info = [
                        f'{task.get_titulo()}',  # Columna para el título
                        f'{task.get_categoria()}',
                        f'{task.get_fecha_in()}',
                        f'{task.get_desc()}',
                        f'{task.get_fecha_fin()}',
                        # Columna para el estado (Completado/No completado)
                        f'{est}',
                        f' '
                    ]
                    # Usar deepcopy para agregar una copia de 'info' a 'data'
                    data.append(deepcopy(info))

            # Establecer el número de filas y columnas en la tabla
            window.tableWidget_2.setRowCount(len(data))
            window.tableWidget_2.setColumnCount(len(data[0])) if data else 0

            # Llenar la tabla con los datos
            for i, row in enumerate(data):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(col)
                    window.tableWidget_2.setItem(i, j, item)
                    
    def llenar_info(windonw):
        windonw.label_16.setText(windonw.us.get_Name()+" "+windonw.us.get_Lastname())
        cont = 0
        for task in windonw.us.get_tasks():
            cont +=1
        windonw.label_17.setText(f'{cont}')
        if windonw.us.get_oscuro():
            windonw.Oscuro.setChecked(True)
            windonw.invertir_colores(True)
        else:
            windonw.Oscuro.setChecked(False)
            windonw.invertir_colores(False)
            
        windonw.Noti.setCurrentIndex( windonw.us.get_priority())
