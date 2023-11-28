import pyodbc
import datetime as dt
import configparser
from typing import List

config = configparser.ConfigParser()
config.read(r'src\Modelo\config.ini')


connection_string = (
    f"Driver={config['Database']['Driver']};"
    f"Server={config['Database']['Server']};"
    f"Database={config['Database']['Database']};"
    f"Uid={config['Database']['Uid']};"
    f"Pwd={config['Database']['Pwd']};"
    f"Encrypt={config['Database']['Encrypt']};"
    f"TrustServerCertificate={config['Database']['TrustServerCertificate']};"
    f"Connection Timeout={config['Database']['ConnectionTimeout']}"
)


class User():
    def __init__(self, uid: int, name: str, lastname: str, username: str, psw: str,
                 priority: int = 2, modo_oscuro: bool = False) -> None:
        self.__id = uid
        self.__name = name
        self.__lastname = lastname
        self.__username = username
        self.__psw = psw
        self.__tasks = []
        self.__priority = priority  # valores entre 0 y 3
        self.__modo_oscuro = modo_oscuro

    def get_Name(self):
        return self.__name
    
    def get_Lastname(self):
        return self.__lastname

    def get_tasks(self) -> List["Tasks"]:
        return self.__tasks

    def get_priority(self) -> int:
        return self.__priority
    
    def get_oscuro(self):
        return self.__modo_oscuro

    def set_oscurodb(self) -> bool:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Users SET modo_oscuro=? WHERE uid=?',
                               True, self.__id)
                conn.commit()
            self.__modo_oscuro = True
            return True
        except pyodbc.Error:
            return False

    def set_clarodb(self) -> bool:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Users SET modo_oscuro=? WHERE uid=?',
                               False, self.__id)
                conn.commit()
            self.__modo_oscuro = False
            return True
        except pyodbc.Error:
            return False

    def set_priority(self, priority) -> bool:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Users SET priority=? WHERE uid=?',
                               priority, self.__id)
                conn.commit()
            self.__priority = priority
            return True
        except pyodbc.Error:
            return False

    def create_task(self, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str, titulo: str) -> bool:
        try:
            from Modelo.Task import Task
            print("Ayuda")
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT MAX(ownid) FROM Tasks WHERE uid=?", self.__id)
                ownid = cursor.fetchone()[0]

            if ownid == None:
                ownid = 0
            else:
                ownid += 1

            tarea = Task(self.__id, ownid, categoria,
                         fecha_in, fecha_fin, desc, titulo)
            self.__tasks.append(tarea)
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Tasks (uid, ownid, categoria, fecha_in, fecha_fin, "desc", terminado, titulo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                               self.__id, ownid, categoria, fecha_in, fecha_fin, desc, False, titulo)
            return True
        except pyodbc.Error:
            return False

    def delete_task(self, id: int) -> bool:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Tasks WHERE ownid=?", id)
                conn.commit()
            for task in self.__tasks:
                if id == task.get_ownid():
                    self.__tasks.remove(task)
                if id < task.get_ownid():
                    task.set_ownid()
            return True
        except pyodbc.Error:
            return False
