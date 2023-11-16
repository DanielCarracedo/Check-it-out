import datetime as dt
import pyodbc
import configparser


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


class Task():
    def __init__(self, uid: int, ownid: int, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str, finished: bool = False) -> None:
        self.__id = uid
        self.__ownid = ownid
        self.__categoria = categoria
        self.__fecha_in = fecha_in
        self.__fecha_fin = fecha_fin
        self.__desc = desc
        self.__finished = finished

    def __repr__(self) -> str:
        return f"Categoria: {self.__categoria}, Descripcion: {self.__desc}"

    def set_completed(self) -> None:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Tasks SET terminado=? WHERE ownid=?',
                           True, self.__ownid)
            conn.commit()
        self.__finished = True

    def edit_task(self, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str):
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Tasks SET categoria=?, fecha_in=?, fecha_fin=?, "desc"=? WHERE ownid=?',
                           categoria, fecha_in, fecha_fin, desc, self.get_ownid())
            conn.commit()
        self.__categoria = categoria
        self.__desc = desc
        self.__fecha_fin = fecha_fin
        self.__fecha_in = fecha_in

    def get_ownid(self) -> int:
        return self.__ownid

    def get_fecha_in(self) -> dt:
        return self.__fecha_in

    def get_fecha_fin(self) -> dt:
        return self.__fecha_fin

    def get_desc(self) -> dt:
        return self.__desc
