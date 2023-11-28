import datetime as dt
from datetime import datetime
import pytest
from unittest.mock import patch, Mock
import sys
sys.path.append("C:/Users/MOJICA/Documents/GitHub/Check-it-out/src")
from Modelo.Task import Task

@patch('pyodbc.connect')
def test_set_completed(mock_connect):

    task = Task(uid=1, ownid=1, categoria='Prueba', fecha_in=dt.datetime.now(),
                fecha_fin=dt.datetime.now(), desc='Descripción de prueba', titulo='Título de prueba')

    result = task.set_completed()

    assert result is True
    mock_connect.assert_called_once()


def test_task_creation():
    fecha_in = datetime(2023, 1, 1)
    fecha_fin = datetime(2023, 1, 10)
    task = Task(uid=1, ownid=1, categoria="Test", fecha_in=fecha_in, fecha_fin=fecha_fin, desc="Test", titulo="Test")

    assert task.get_ownid() == 1
    assert task.get_categoria() == "Test"
    assert task.get_fecha_in() == fecha_in
    assert task.get_fecha_fin() == fecha_fin
    assert task.get_desc() == "Test"
    assert task.get_titulo() == "Test"
    assert not task.get_finished()
    
@patch('pyodbc.connect')
def test_set_uncompleted(mock_connect):

    task = Task(uid=1, ownid=1, categoria='Prueba', fecha_in=dt.datetime.now(),
                fecha_fin=dt.datetime.now(), desc='Descripción de prueba', titulo='Título de prueba')

    result = task.set_uncompleted()

    assert result is True
    mock_connect.assert_called_once()

@patch('pyodbc.connect')
def test_edit_task(mock_connect):
    
    task = Task(uid=1, ownid=1, categoria='Prueba', fecha_in=dt.datetime.now(),
                fecha_fin=dt.datetime.now(), desc='Descripción de prueba', titulo='Título de prueba')

    result = task.edit_task(categoria='NuevaCategoria', fecha_in=dt.datetime.now(),
                            fecha_fin=dt.datetime.now(), desc='NuevaDescripción', titulo='NuevoTítulo')

    assert result is True
    mock_connect.assert_called_once()

@patch('pyodbc.connect')
def test_set_ownid(mock_connect):

    task = Task(uid=1, ownid=1, categoria='Prueba', fecha_in=dt.datetime.now(),
                fecha_fin=dt.datetime.now(), desc='Descripción de prueba', titulo='Título de prueba')

    result = task.set_ownid()

    assert result is True
    mock_connect.assert_called_once()