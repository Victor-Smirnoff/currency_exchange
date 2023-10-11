import sqlite3
import os
from post_performer import PostPerformer
from config import Config
from get_performer_exchange_rates import GetPerformerExchangeRates


class PostPerformerExchangeRates(PostPerformer):
    """
    Класс принимает в обработку POST запросы в таблицу ExchangeRates на добавление нового курса
    """

    def __init__(self, path, command="POST"):
        """
        Инициализатор класса PostPerformerExchangeRates
        :param path: путь запроса
        :param command: HTTP метод запроса - POST
        """
        super().__init__(path, command)

    def post_exchange_rates(self, baseCurrencyCode, targetCurrencyCode, rate):
        """
        Метод добавляет новый обменный курс в таблицу ExchangeRates
        :param baseCurrencyCode: базвая валюта
        :param targetCurrencyCode: целевая валюта
        :param rate: обменный курс
        :return: кортеж из двух элементов:
        индекс 0 - код HTTP ответа
        индекс 1 - JSON-объект (сериализованный словарь)
        HTTP коды ответов:
        Успех - 200
        Отсутствует нужное поле формы - 400
        Валютная пара с таким кодом уже существует - 409
        Ошибка (например, база данных недоступна) - 500
        """
        currency_codes = baseCurrencyCode + targetCurrencyCode
        # если коды не переданы или длина передаваемой строки не равно 6 символам
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            query_data = {"message": f"Ошибка - {response_code} (Отсутствует нужное поле формы)"}
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

                        BaseCurrencyId = cursor.execute(query, (baseCurrencyCode, )).fetchone()[0]
                        TargetCurrencyId = cursor.execute(query, (targetCurrencyCode, )).fetchone()[0]

                        # открываем файл с SQL-запросом на чтение таблицы ExchangeRates (добавление нового обменного курса)
                        with open("db/POST_exchange_rate.txt", "r") as file:
                            query = file.read()

                        try:
                            cursor.execute(query, (BaseCurrencyId, TargetCurrencyId, rate))
                            db.commit()
                            get_exchange_rate = GetPerformerExchangeRates(self.path)
                            response_code, query_data = get_exchange_rate.get_certain_exchange_rate(currency_codes)
                            return (response_code, query_data)

                        except sqlite3.IntegrityError as e:
                            response_code = 409
                            query_data = {"message": f"Ошибка - {e}. Валютная пара с таким кодом уже существует - 409"}

                except sqlite3.IntegrityError:
                    response_code = 500
                    query_data = {"message": f"Ошибка - {response_code} (база данных недоступна)"}
            else:
                response_code = 500
                query_data = {"message": f"Ошибка - {response_code} (файла базы данных нет)"}

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        return (response_code, query_data)