import pyodbc
import configparser
from User import User
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


class Chekitout():
    def __init__(self) -> None:
        pass

    # Recibe los datos encriptados
    def register_user(self, name: str, lastname: str, username: str, psw: str) -> bool:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(uid) FROM Users")
            uid = cursor.fetchone()[0]
            if uid == None:
                uid = 0
            else:
                uid += 1

            cursor.execute("INSERT INTO Users (uid, name, lastname, username, psw) VALUES (?, ?, ?, ?, ?)",
                           uid, name, lastname, username, psw)
        return True

    # Recibe los datos encriptados
    def check_user(self, username: str, psw: str) -> bool:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COUNT(*) FROM Users WHERE username=? AND psw=?", username, psw)
            result = cursor.fetchone()
        # Si el resultado es 1, las credenciales son correctas
        return result[0] == 1

    # Ejecutar este metodo SOLO si check_user devuelve true
    def create_session(self, username: str) -> "User()":
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE username=?", username)
            resultado = cursor.fetchone()
            # info de task
            cursor.execute("SELECT * FROM Tasks WHERE uid=?", resultado.uid)
            tasks = cursor.fetchall()

        session = User(resultado.uid, resultado.name,
                       resultado.lastname, resultado.username, resultado.psw)
        tareas = [Task(resultado.uid, task.ownid, task.categoria,
                       task.fecha_in, task.fecha_fin, task.desc) for task in tasks]
        session.get_tasks().extend(tareas)
        return session
