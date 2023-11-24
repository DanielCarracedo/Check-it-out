import pyodbc
import configparser
import hashlib
from datetime import datetime

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


def return_hash(text):
    h = hashlib.new("SHA256")
    h.update(text.encode())
    return h.hexdigest()


class Chekitout():
    def __init__(self) -> None:
        pass

    def register_user(self, name: str, lastname: str, username: str, psw: str) -> bool:
        try:
            hashed_username = return_hash(username)
            psw = return_hash(psw)
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(uid) FROM Users")
                uid = cursor.fetchone()[0]
                if uid == None:
                    uid = 0
                else:
                    uid += 1
                x = self.check_username(username)
                if x == False:
                    cursor.execute("INSERT INTO Users (uid, name, lastname, username, psw, priority, modo_oscuro) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           uid, name, lastname, hashed_username, psw, 2, False)
                    return True
                else: 
                    return False
        except pyodbc.Error:
            return 1 #Si retorna 1 y no un booleano entonces hubo un error en el servidor

    def check_user(self, username: str, psw: str) -> bool:
        try: 
            username = return_hash(username)
            psw = return_hash(psw)
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM Users WHERE username=? AND psw=?", username, psw)
                result = cursor.fetchone()
            # Si el resultado es 1, las credenciales son correctas
            if result[0] == 1:
                return True
            else:
                return False
        except pyodbc.Error:
            #Si retorna 1 y no un booleano entonces hubo un error en el servidor
            return 1
                
    def check_username(self, username: str) -> bool:
        try: 
            username = return_hash(username)
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM Users WHERE username=?", username)
                result = cursor.fetchone()
                if result[0] > 0:
                    return True
                else:
                    return False
        except pyodbc.Error:
            #Si retorna 1 y no un booleano entonces hubo un error en el servidor
            return 1
    
    # Ejecutar este metodo SOLO si check_user devuelve true
    def create_session(self, username: str) -> "User()":
        try:
            from User import User
            from Task import Task
            username = return_hash(username)
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Users WHERE username=?", username)
                resultado = cursor.fetchone()
                # info de task
                cursor.execute("SELECT * FROM Tasks WHERE uid=?", resultado.uid)
                tasks = cursor.fetchall()

            session = User(resultado.uid, resultado.name,
                       resultado.lastname, resultado.username, resultado.psw, resultado.priority, resultado.modo_oscuro)
            tareas = [Task(resultado.uid, task.ownid, task.categoria,
                       task.fecha_in, task.fecha_fin, task.desc, task.terminado, task.titulo) for task in tasks]
            session.get_tasks().extend(tareas)
            return session
        
        except pyodbc.Error:
            return False

return_hash("Hola")