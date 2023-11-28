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
    def __init__(self, uid: int, ownid: int, categoria: str, fecha_in: dt, 
                fecha_fin: dt, desc: str, titulo: str, finished: bool = False) -> None:
        self.__id = uid
        self.__ownid = ownid
        self.__categoria = categoria
        self.__fecha_in = fecha_in
        self.__fecha_fin = fecha_fin
        self.__desc = desc
        self.__finished = finished
        self.__titulo = titulo

    def __repr__(self) -> str:
        return f"Categoria: {self.__categoria}, Descripcion: {self.__desc}"

    def set_completed(self) -> bool:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Tasks SET terminado=? WHERE ownid=?',
                           True, self.__ownid)
                conn.commit()
            self.__finished = True
            return True
        except pyodbc.Error:
            return False

    def set_uncompleted(self) -> bool:
        try: 
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Tasks SET terminado=? WHERE ownid=?',
                           False, self.__ownid)
                conn.commit()
            self.__finished = False
            return True
        except pyodbc.Error:
            return False

    def edit_task(self, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str, titulo: str) -> bool:
        try:
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Tasks SET categoria=?, fecha_in=?, fecha_fin=?, "desc"=?, titulo=? WHERE ownid=?',
                           categoria, fecha_in, fecha_fin, desc, titulo, self.get_ownid())
                conn.commit()
            self.__categoria = categoria
            self.__desc = desc
            self.__fecha_fin = fecha_fin
            self.__fecha_in = fecha_in
            self.__titulo = titulo
            return True
        except pyodbc.Error:
            return False
    
    def set_ownid(self):
        try:
            new_id = self.__ownid-1
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('UPDATE Tasks SET ownid=? WHERE ownid=?',
                           new_id, self.__ownid)
                conn.commit()
            self.__ownid = new_id

            return True
        except pyodbc.Error:
            return False

    def get_ownid(self) -> int:
        return self.__ownid
    
    def get_finished(self) -> bool:
        return self.__finished
    
    def get_fecha_in(self) -> dt:
        return self.__fecha_in

    def get_fecha_fin(self) -> dt:
        return self.__fecha_fin

    def get_desc(self) -> str:
        return self.__desc

    def get_titulo(self) -> str:
        return self.__titulo
    
    def get_categoria(self)->str:
        return self.__categoria
