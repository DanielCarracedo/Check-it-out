import pyodbc
import configparser
from datetime import datetime
from Modelo.sist import Chekitout
from Modelo.User import User
from Modelo.Task import Task
import pickle

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
                #cursor.execute("DELETE FROM Users")

                # Vaciar la tabla Tasks
                cursor.execute("DELETE FROM Tasks")

                print("Ambas tablas se han vaciado correctamente.")

        except pyodbc.Error as e:
            print(f"Error al vaciar las tablas: {e}")



print_users_and_tasks()