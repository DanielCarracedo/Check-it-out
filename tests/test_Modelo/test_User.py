import pytest
import datetime as dt
from unittest.mock import patch, Mock
import datetime
import sys
sys.path.append("C:/Users/MOJICA/Documents/GitHub/Check-it-out/src")
from Modelo.User import User
from Modelo.Task import Task

@pytest.fixture
def sample_user():
    return User(uid=1, name="Juan", lastname="M", username="JuanM", psw="hashed_password", priority=2, modo_oscuro=False)

def test_user_creation(sample_user):
    assert sample_user.get_Name() == "Juan"
    assert sample_user.get_priority() == 2

@patch('pyodbc.connect')
def test_create_task(mock_connect):
    user = User(uid=1, name='Juan', lastname='M', username='JuanM', psw='password')

    fecha_in = dt.datetime.now()
    fecha_fin = fecha_in + dt.timedelta(days=7)

    result = user.create_task(categoria='Trabajo', fecha_in=fecha_in, fecha_fin=fecha_fin, desc='Hacer tarea', titulo='Tarea 1')

    assert result is True
    mock_connect.assert_called()

@patch('pyodbc.connect')
def test_set_priority(mock_connect):
    user = User(uid=1, name='Juan', lastname='M', username='JuanM', psw='password')

    result = user.set_priority(priority=1)

    assert result is True
    mock_connect.assert_called_once()

@patch('pyodbc.connect')
def test_set_clarodb(mock_connect):
    user = User(uid=1, name='JuanM', lastname='M', username='JuanM', psw='password')

    result = user.set_clarodb()

    assert result is True
    mock_connect.assert_called_once()

@patch('pyodbc.connect')
def test_set_oscurodb(mock_connect):
    user = User(uid=1, name='Juan', lastname='M', username='JuanM', psw='password')

    result = user.set_oscurodb()

    assert result is True
    mock_connect.assert_called_once()

@patch('pyodbc.connect')
def test_delete_task(mock_connect):
    user = User(uid=1, name='Juan', lastname='M', username='JuanM', psw='password')
    fecha_in = dt.datetime.now()
    fecha_fin = fecha_in + dt.timedelta(days=7)
    task = user.create_task(categoria='Trabajo', fecha_in=fecha_in, fecha_fin=fecha_fin, desc='Hacer tarea', titulo='Tarea 1')

    real_task = Task(uid=1, ownid=1, categoria='Trabajo', fecha_in=fecha_in, fecha_fin=fecha_fin, desc='Hacer tarea', titulo='Tarea 1')

    user._User__tasks = [real_task]

    result = user.delete_task(id=1)

    assert result is True
    mock_connect.assert_called()