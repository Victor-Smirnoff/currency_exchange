from exchange_repository import ExchangeRepository
from model.exchange_rate import ExchangeRate
from model.exchange_response import ExchangeResponse
from model.error_response import ErrorResponse
import sqlite3
from config.config import Config


class DaoExchangeRepository(ExchangeRepository):
    """
    Класс для выполнения основных операций в БД над таблицей ExchangeRates
    """

    def find_by_codes(self, currency_codes):
        """
        Метод возвращает данные по одному конкретному курсу валют
        Принимает строку с идущими подряд кодами валют в адресе запроса
        :param currency_codes: строка с идущими подряд кодами валют (в адресе запроса)
        :return: объект класса ExchangeRate или объект класса ErrorResponse
        """