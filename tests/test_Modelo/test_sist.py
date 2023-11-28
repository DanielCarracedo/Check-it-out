import datetime as dt
import pytest
from unittest.mock import patch, Mock
import sys
sys.path.append("C:/Users/MOJICA/Documents/GitHub/Check-it-out/src")
from Modelo.sist import Chekitout

@patch('pyodbc.connect')
def test_create_session(mock_connect):
    chekitout = Chekitout()

    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = (1, 'Juan', 'M', 'hash_username', 'hash_password', 2, False)
    mock_connect.return_value.cursor.return_value = mock_cursor

    result = chekitout.create_session(username='JuanM')
