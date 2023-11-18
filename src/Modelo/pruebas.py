import pyodbc
import configparser
from datetime import datetime
from sist import Chekitout
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



def print_users_and_tasks():
        try:
            # Conectar a la base de datos
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()

                # Obtener información de la tabla Users
                cursor.execute("SELECT * FROM Users")
                users_data = cursor.fetchall()

                # Imprimir información de la tabla Users
                print("Tabla Users:")
                print("uid | name | lastname | username | psw | priority | modo_oscuro")
                for row in users_data:
                    print(row)

                # Obtener información de la tabla Tasks
                cursor.execute("SELECT * FROM Tasks")
                tasks_data = cursor.fetchall()

                # Imprimir información de la tabla Tasks
                print("\nTabla Tasks:")
                print("uid | ownid | categoria | fecha_in | fecha_fin | desc | terminado | titulo")
                for row in tasks_data:
                    print(row)

        except pyodbc.Error as e:
            print(f"Error al imprimir la información: {e}")

def empty_tables():
        try:
            # Conectar a la base de datos
            with pyodbc.connect(connection_string) as conn:
                cursor = conn.cursor()

                # Vaciar la tabla Users
                cursor.execute("DELETE FROM Users")

                # Vaciar la tabla Tasks
                cursor.execute("DELETE FROM Tasks")

                print("Ambas tablas se han vaciado correctamente.")

        except pyodbc.Error as e:
            print(f"Error al vaciar las tablas: {e}")

prueba = Chekitout()

x1 = prueba.register_user("pedro", "sanchez", "pedrito09", "pedritokul123")
if x1 == True:
    x = prueba.check_user("pedrito09", "pedritokul123")
    fecha_in = datetime.now()
    fecha_fin = datetime(2015, 3, 24)
    if x == True:
        user = prueba.create_session("pedrito09")
        user.set_priority(0)
        user.create_task("gym", fecha_in, fecha_fin, "descripcion bien perrona", "Sacar al perro")
        user.create_task("tarea eliminable", fecha_in, fecha_fin, "me voy eliminado", "ahhhhhhhh")
        user.delete_task(1)
        user.set_oscurodb()
        for task in user.get_tasks():
            if task.get_ownid() == 0:
                task.edit_task("gym", fecha_in, fecha_fin, "descripcion bien perrona", "Sacar al perrito")
                task.set_completed
else:
    print("ombe este man ya existe")

print_users_and_tasks()