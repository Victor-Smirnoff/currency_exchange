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
        # если коды не переданы или длина передаваемой строки не равно 6 символам
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            message = f"Ошибка - {response_code} (Коды валют отсутствуют в адресе или длина двух кодов валют не равна 6)"
            query_data = ErrorResponse(response_code, message)
        else:
            baseCurrency = currency_codes[:3]
            targetCurrency = currency_codes[3:]

            try:
                with sqlite3.connect(Config.db_file) as db:
                    cursor = db.cursor()

                    # открываем файл с SQL-запросом на чтение таблицы ExchangeRates (получение таблицы всех валют)
                    with open("../db/GET_exchange_rate.txt", "r") as file:
                        query = file.read()

                    result_data = cursor.execute(query, (baseCurrency, targetCurrency,)).fetchone()

                    # если результат SQL-запроса не пуст, то формируем объект класса ExchangeRate
                    if result_data:
                        ID, BaseCurrencyId, TargetCurrencyId, Rate = result_data[0], result_data[1], result_data[2], result_data[3]
                        query_data = ExchangeRate(ID, BaseCurrencyId, TargetCurrencyId, Rate)

                    # иначе если результат SQL-запроса пуст, то response_code = 404
                    else:
                        response_code = 404
                        message = f"Ошибка - Обменный курс для пары не найден - {response_code}"
                        query_data = ErrorResponse(response_code, message)

            except sqlite3.IntegrityError:
                response_code = 500
                message = f"Ошибка - {response_code} (база данных недоступна)"
                query_data = ErrorResponse(response_code, message)

        return query_data

    def find_by_codes_with_usd_base(self, code):
        """
        Метод ищет обменный курс целевой валюты при условии, что базовая валюта - это USD
        :param code: код целевой валюты
        :return: объект класса ExchangeRate или объект класса ErrorResponse
        """
        # если коды не переданы или длина передаваемой строки не равно 6 символам
        if not code or len(code) != 3:
            response_code = 400
            message = f"Ошибка - {response_code} (Коды валют отсутствуют в адресе или длина двух кодов валют не равна 6)"
            query_data = ErrorResponse(response_code, message)
        else:
            baseCurrency = "USD"
            targetCurrency = code

            try:
                with sqlite3.connect(Config.db_file) as db:
                    cursor = db.cursor()

                    # открываем файл с SQL-запросом на чтение таблицы ExchangeRates (получение таблицы всех валют)
                    with open("../db/GET_exchange_rate.txt", "r") as file:
                        query = file.read()

                    result_data = cursor.execute(query, (baseCurrency, targetCurrency,)).fetchone()

                    # если результат SQL-запроса не пуст, то формируем объект класса ExchangeRate
                    if result_data:
                        ID, BaseCurrencyId, TargetCurrencyId, Rate = result_data[0], result_data[1], result_data[2], result_data[3]
                        query_data = ExchangeRate(ID, BaseCurrencyId, TargetCurrencyId, Rate)

                    # иначе если результат SQL-запроса пуст, то response_code = 404
                    else:
                        response_code = 404
                        message = f"Ошибка - Обменный курс для пары не найден - {response_code}"
                        query_data = ErrorResponse(response_code, message)

            except sqlite3.IntegrityError:
                response_code = 500
                message = f"Ошибка - {response_code} (база данных недоступна)"
                query_data = ErrorResponse(response_code, message)

        return query_data