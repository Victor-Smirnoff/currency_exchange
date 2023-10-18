"""
Здесь описан класс для хранения данных по расчёту перевода определённого количества средств из одной валюты в другую
"""


class ErrorResponse:
    """
    Класс для хранения данных по расчёту перевода определённого количества средств из одной валюты в другую
    """
    def __init__(self, baseCurrency, targetCurrency, rate, amount, convertedAmount):
        """
        :param baseCurrency: объект с данными базовой валюты
        :param targetCurrency: объект с данными целевой валюты
        :param rate: обменный курс
        :param amount: количество базовой валюты
        :param convertedAmount: полученное количество целевой валюты
        """
        self.baseCurrency = baseCurrency
        self.targetCurrency = targetCurrency
        self.rate = rate
        self.amount = amount
        self.convertedAmount = convertedAmount