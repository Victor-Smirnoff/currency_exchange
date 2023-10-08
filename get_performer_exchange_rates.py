import sqlite3
import os
from get_performer import GetPerformer
from config import Config


class GetPerformerExchangeRates(GetPerformer):
    """
    Класс принимает в обработку GET запросы в таблицу ExchangeRates на получение всех курсов
    Класс принимает в обработку GET запросы в таблицу ExchangeRates на получение конкретного курса валюты
    Класс принимает в обработку GET запросы в таблицу ExchangeRates на
    расчёт перевода определённого количества средств из одной валюты в другую
    """

    def __init__(self, path, command="GET"):
        """
        Инициализатор класса GetPerformerExchangeRates
        :param path: путь запроса
        :param command: HTTP метод запроса - GET
        """
        super().__init__(path, command)

    def get_all_exchange_rates(self):
        """
        Метод для получения списка всех обменных курсов валют из таблицы ExchangeRates
        Метод возвращает кортеж в виде:
        индекс 0 - код HTTP ответа
        индекс 1 - JSON-объект (сериализованный список со словарями)
        :return: tuple
        """
        # проверить наличие файла базы данных перед созданием подключения
        if os.path.exists(Config.db_file):
            try:
                with sqlite3.connect(Config.db_file) as db:
                    cursor = db.cursor()

                    # открываем файл с SQL-запросом на чтение таблицы Currencies (получение таблицы всех валют)
                    with open("db/GET_exchange_rates.txt", "r") as file:
                        query = file.read()

                    response_code = 200
                    query_data = cursor.execute(query).fetchall()

                    # # список названий колонок из выполненного SQL-запроса. это будут преобразованные ключи словаря
                    # column_names = [description[0] for description in cursor.description]

                    # # теперь необходимо вызвать метод, который преобразует полученные данные в нужный нам список
                    # query_data = self.convert_query_data_currencies(column_names, query_data)

            except sqlite3.IntegrityError:
                response_code = 500
                query_data = [f"Ошибка - {response_code} (например, база данных недоступна)"]
        else:
            response_code = 500
            query_data = [f"Ошибка - {response_code} (файла базы данных нет)"]

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        # return (response_code, query_data)
        return query_data


res_performer = GetPerformerExchangeRates("/exchangeRates")

data = res_performer.perform_handling()

print(data)