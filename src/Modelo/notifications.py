from plyer import notification
from datetime import datetime, timedelta
import time


def notificacion(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Checkitout",
        # Puedes proporcionar la ruta a un icono personalizado
        app_icon="src/Modelo/iconochekitout.ico",
        timeout=10,  # Duración de la notificación en segundos
    )


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
            notificacion("Fecha Cercana",
                         f"Te queda 1 hora para '{task.get_descripcion()}'")
        elif timedelta(hours=6) < tiempo_restante < timedelta(hours=12):
            notificacion(
                "Fecha Cercana", f"Te quedan menos de 12 horas para '{task.get_descripcion()}'")

    # Verificar si hay tareas pendientes para enviar notificación
    if cont > 0 and x == 1:
        notificacion(
            "Tareas", f"Le queda 10% del tiempo para completar {cont} tareas")
        time.sleep(90 * 60)

    elif cont > 0 and x == 2:
        notificacion(
            "Tareas", f"Le queda 25% del tiempo para completar {cont} tareas")
        time.sleep(60*60)

    elif cont > 0 and x == 3:
        notificacion(
            "Tareas", f"Le queda la mitad del tiempo para completar {cont} tareas")
        time.sleep(60*60)
