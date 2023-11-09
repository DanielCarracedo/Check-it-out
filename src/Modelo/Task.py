import datetime as dt


class Task():
    def __init__(self, uid: int, ownid: int, categoria: str, fecha_in: dt, fecha_fin: dt, desc: str) -> None:
        self.__id = uid
        self.__ownid = ownid
        self.__categoria = categoria
        self.__fecha_in = fecha_in
        self.__fecha_fin = fecha_fin
        self.__desc = desc

    def get_ownid(self):
        return self.__ownid
