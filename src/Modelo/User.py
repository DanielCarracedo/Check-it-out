import pyodbc
import datetime as dt
import configparser
from Task import Task

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
    def __init__(self, uid: int, name: str, lastname: str, username: str, psw: str) -> None:
        self.__id = uid
        self.__name = name
        self.__lastname = lastname
        self.__username = username
        self.__psw = psw
        self.__tasks = []

    def get_tasks(self):
        return self.__tasks

    def create_task(self, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str) -> bool:
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
            cursor.execute('INSERT INTO Tasks (uid, ownid, categoria, fecha_in, fecha_fin, "desc") VALUES (?, ?, ?, ?, ?, ?)',
                           self.__id, ownid, categoria, fecha_in, fecha_fin, desc)
        return True

    def delete_task(self, id: int) -> bool:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Tasks WHERE ownid=?", id)
            conn.commit()
        for task in self.__tasks:
            if id == task.get_ownid():
                self.__tasks.remove(task)

    def edit_task(self, ownid: int, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str):
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Tasks SET categoria=?, fecha_in=?, fecha_fin=?, "desc"=? WHERE ownid=?',
                           categoria, fecha_in, fecha_fin, desc, ownid)
            conn.commit()
