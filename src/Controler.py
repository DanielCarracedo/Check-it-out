from Modelo.Task import Task
from Modelo.sist import Chekitout
from Modelo.User import User

class Controller():
    
    def __init__(self) -> None:
        
        pass
    
    def Register(sel, name: str, lastname: str, username: str, psw: str):
        sis = Chekitout()
        sis.register_user(name, lastname,username, psw)
    
    def confirm_user(self, username: str, psw: str)->bool:
        sis = Chekitout()
        x = sis.check_user(username, psw)  
        return x      