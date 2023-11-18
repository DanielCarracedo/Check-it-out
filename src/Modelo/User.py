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
    def __init__(self, uid: int, name: str, lastname: str, username: str, psw: str, priority: int = 2) -> None:
        self.__id = uid
        self.__name = name
        self.__lastname = lastname
        self.__username = username
        self.__psw = psw
        self.__tasks = []
        self.__priority = priority

    def get_tasks(self) -> List["Tasks"]:
        return self.__tasks

    def get_priority(self) -> int:
        return self.__priority

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

    def create_task(self, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str) -> bool:
        try:
            from Task import Task
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(ownid) FROM Tasks")
                ownid = cursor.fetchone()[0]

            if ownid == None:
                ownid = 0
            else:
                ownid += 1

            tarea = Task(self.__id, ownid, categoria, fecha_in, fecha_fin, desc)
            self.__tasks.append(tarea)
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Tasks (uid, ownid, categoria, fecha_in, fecha_fin, "desc", terminado) VALUES (?, ?, ?, ?, ?, ?, ?)',
                           self.__id, ownid, categoria, fecha_in, fecha_fin, desc, False)
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
            return True
        except pyodbc.Error:
            return False