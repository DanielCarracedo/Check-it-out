from win10toast import ToastNotifier
from datetime import datetime, timedelta
import time


def notification(title, message):
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10,
                       icon_path=r"src/Modelo/iconochekitout.ico")


def send_notification(user="User"):
    x = user.get_priority()
    cont = 0

    for task in user.get_tasks():
        f1 = task.get_fecha_in()
        f2 = task.get_fecha_fin()
        diferencia = f2 - f1
        tiempo_restante = f2 - datetime.now()

        # Verificar tiempo restante y prioridad
        if x == 1 and tiempo_restante < (diferencia * 0.1):
            cont += 1
        elif x == 2 and tiempo_restante < (diferencia * 0.25):
            cont += 1
        elif x == 3 and tiempo_restante < (diferencia * 0.5):
            cont += 1

        # Verificar notificaciones para tareas cercanas
        if tiempo_restante < timedelta(hours=1):
            notification("Fecha Cercana",
                         f"Te queda 1 hora para '{task.get_descripcion()}'")
        elif timedelta(hours=6) < tiempo_restante < timedelta(hours=12):
            notification(
                "Fecha Cercana", f"Te quedan menos de 12 horas para '{task.get_descripcion()}'")

    # Verificar si hay tareas pendientes para enviar notificación
    if cont > 0 and x == 1:
        notification(
            "Tareas", f"Le queda 10% del tiempo para completar {cont} tareas")
        time.sleep(90 * 60)

    elif cont > 0 and x == 2:
        notification(
            "Tareas", f"Le queda 25% del tiempo para completar {cont} tareas")
        time.sleep(60*60)

    elif cont > 0 and x == 3:
        notification(
            "Tareas", f"Le queda la mitad del tiempo para completar {cont} tareas")
        time.sleep(60*60)


notification("esto es un titulo", "y esto un super mensaje")
