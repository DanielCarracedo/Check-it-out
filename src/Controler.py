from Modelo.Task import Task
from Modelo.sist import Chekitout
from Modelo.User import User
import datetime as dt
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
    
    def new_task(self, user:"User", categoria: str, fecha_in: dt, fecha_fin: dt, desc: str, titulo: str)->bool:
        X=user.create_task(categoria,fecha_in,fecha_fin,desc,titulo)
        print(X)