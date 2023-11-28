import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import sys
sys.path.append("C:/Users/MOJICA/Documents/GitHub/Check-it-out/src")
from Modelo.User import User
from Modelo.notifications import notificacion, proximity_notification, send_notification

@pytest.fixture
def user_mock():
    return MagicMock()

@pytest.fixture
def task_mock():
    return MagicMock()

from plyer import notification

def test_notificacion(mocker):
    mocker.patch('plyer.notification.notify')
    notificacion("Title", "Message")
    notification.notify.assert_called_once_with(
        title="Title",
        message="Message",
        app_name="Checkitout",
        app_icon="src/Modelo/iconochekitout.ico",
        timeout=10
    )


def test_proximity_notification(user_mock, task_mock, mocker):
    task_mock.get_fecha_fin.return_value = datetime.now() + timedelta(seconds=1800) 
    task_mock.get_titulo.return_value = "TaskTitle"
    task_mock.get_finished.return_value = False
    user_mock.get_priority.return_value = 1
    user_mock.get_tasks.return_value = [task_mock]

    mocker.patch('time.sleep')
    proximity_notification(user_mock)

    mocker.stopall()

def test_send_notification(user_mock, task_mock, mocker):
    task_mock.get_fecha_in.return_value = datetime.now()
    task_mock.get_fecha_fin.return_value = datetime.now() + timedelta(days=1)
    task_mock.get_finished.return_value = False
    user_mock.get_priority.return_value = 1
    user_mock.get_tasks.return_value = [task_mock]

    mocker.patch('time.sleep') 
    send_notification(user_mock)
    
    mocker.stopall()

