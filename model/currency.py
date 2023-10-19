"""
Здесь описан класс для хранения данных по каждой валюте
"""


class Currency:
    """
    Класс для хранения данных по каждой валюте
    """
    def __init__(self, ID, FullName, Code, Sign):
        """
        :param ID: Айди валюты
        :param FullName: Полное имя валюты
        :param Code: Код валюты
        :param Sign: Символ валюты
        """
        self.ID = ID
        self.FullName = FullName
        self.Code = Code
        self.Sign = Sign

    def __str__(self):
        return str({"id": self.ID, "name": self.FullName, "code": self.Code, "sign": self.Sign})