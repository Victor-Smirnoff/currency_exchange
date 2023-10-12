import sqlite3
import os
from patch_performer import PatchPerformer
from config import Config
from get_performer_exchange_rates import GetPerformerExchangeRates


class PatchPerformerExchangeRates(PatchPerformer):
    """
    Класс принимает в обработку PATCH запросы в таблицу ExchangeRates на добавление нового курса
    """

    def __init__(self, path, command="PATCH"):
        """
        Инициализатор класса PatchPerformerExchangeRates
        :param path: путь запроса
        :param command: HTTP метод запроса - PATCH
        """
        super().__init__(path, command)

    def patch_exchange_rates(self, rate, currency_codes):
        """
        Метод выполняет обработку PATCH запроса на обновдление данных поля rate в таблице ExchangeRates
        :param rate: обменный курс
        :param currency_codes: коды валют - Валютная пара задаётся идущими подряд кодами валют
        :return: кортеж из двух элементов:
        индекс 0 - код HTTP ответа
        индекс 1 - JSON-объект (сериализованный словарь)
        HTTP коды ответов:
        Успех - 200
        Отсутствует нужное поле формы - 400
        Валютная пара отсутствует в базе данных - 404
        Ошибка (например, база данных недоступна) - 500
        """
        baseCurrencyCode = currency_codes[:3]
        targetCurrencyCode = currency_codes[3:]
        # если коды не переданы или длина передаваемой строки не равно 6 символам или не передан rate
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            query_data = {"message": f"Ошибка - {response_code} (Отсутствует нужное поле формы - коды валют в адресе запроса {self.path})"}
        elif not rate:
            response_code = 400
            query_data = {"message": f"Ошибка - {response_code} (Отсутствует нужное поле формы - 'rate')"}
        else:
            # проверить наличие файла базы данных перед созданием подключения
            if os.path.exists(Config.db_file):
                try:
                    with sqlite3.connect(Config.db_file) as db:
                        cursor = db.cursor()

                        # теперь необходимо по коду валюты получить её ID
                        # открываем файл с SQL-запросом на чтение таблицы Currencies (взять ID валюты по её коду)
                        with open("db/GET_ID_of_currency_from_code.txt", "r") as file:
                            query = file.read()

                        BaseCurrencyId = cursor.execute(query, (baseCurrencyCode,)).fetchone()[0]
                        TargetCurrencyId = cursor.execute(query, (targetCurrencyCode,)).fetchone()[0]

                        # открываем файл с SQL-запросом на чтение таблицы ExchangeRates (изменение существующего обменного курса)
                        with open("db/PATCH_exchange_rate.txt", "r") as file:
                            query = file.read()

                        cursor.execute(query, (rate, BaseCurrencyId, TargetCurrencyId))
                        db.commit()
                        get_exchange_rate = GetPerformerExchangeRates(self.path)
                        response_code, query_data = get_exchange_rate.get_certain_exchange_rate(currency_codes)
                        if response_code == 404:
                            query_data = {"message": f"Ошибка: Валютная пара {baseCurrencyCode}-{targetCurrencyCode} отсутствует в базе данных - {response_code}"}
                        else:
                            return (response_code, query_data)

                except sqlite3.IntegrityError:
                    response_code = 500
                    query_data = {"message": f"Ошибка - {response_code} (база данных недоступна)"}
            else:
                response_code = 500
                query_data = {"message": f"Ошибка - {response_code} (файла базы данных нет)"}

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        return (response_code, query_data)