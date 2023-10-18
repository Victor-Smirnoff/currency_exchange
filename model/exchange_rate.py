"""
Здесь описан класс для хранения данных по каждому обменному курсу
"""


class ExchangeRate:
    """
    Класс для хранения данных по каждому обменному курсу
    """
    def __init__(self, ID, BaseCurrencyId, TargetCurrencyId, Rate):
        """
        :param ID: Айди курса обмена
        :param BaseCurrencyId: ID базовой валюты
        :param TargetCurrencyId: ID целевой валюты
        :param Rate: Курс обмена единицы базовой валюты к единице целевой валюты
        """
        self.ID = ID
        self.BaseCurrencyId = BaseCurrencyId
        self.TargetCurrencyId = TargetCurrencyId
        self.Rate = Rate