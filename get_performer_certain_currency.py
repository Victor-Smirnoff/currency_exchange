import sqlite3
import os
from get_performer import GetPerformer


class GetPerformerCertainCurrency(GetPerformer):
    """
    Класс принимает в обработку GET запросы в таблицу Currencies на получение конкретной валюты
    """

    def __init__(self, path, command="GET"):
        """
        Инициализатор класса GetPerformerCertainCurrency
        :param path: путь запроса
        :param command: HTTP метод запроса - GET
        """
        super().__init__(path, command)

    def get_certain_currency(self, currency_code):
        """
        Метод возвращает данные по одной конкретной валюте
        кортеж в виде:
        индекс 0 - код HTTP ответа
        индекс 1 - JSON-объект (сериализованный словарь с данными конкретной валюты из БД)
        :return: tuple
        HTTP коды ответов:
        Успех - 200
        Код валюты отсутствует в адресе - 400
        Валюта не найдена - 404
        Ошибка (например, база данных недоступна) - 500
        """
        if not currency_code:
            response_code = 400
            query_data = [f"Код валюты отсутствует в адресе - {response_code}"]
        else:
            # проверить наличие файла базы данных перед созданием подключения
            if os.path.exists("db/database.db"):
                try:
                    with sqlite3.connect("db/database.db") as db:
                        cursor = db.cursor()

                        # открываем файл с SQL-запросом на чтение таблицы Currencies (получение таблицы всех валют)
                        with open("db/GET_currency.txt", "r") as file:
                            query = file.read()

                        query_data = cursor.execute(query, (currency_code,)).fetchone()

                        # если результат SQL-запроса не пуст, то response_code = 200 и формируем корректный ответ query_data
                        if query_data:
                            response_code = 200

                            # список названий колонок из выполненного SQL-запроса. это будут преобразованные ключи словаря
                            column_names = [description[0] for description in cursor.description]

                            # теперь необходимо вызвать метод, который преобразует полученные данные в нужный нам словарь
                            query_data = self.convert_query_data_certain_currency(column_names, query_data)

                        # иначе если результат SQL-запроса пуст, то  response_code = 404
                        else:
                            response_code = 404
                            query_data = [f"Ошибка - Валюта не найдена - {response_code}"]

                except sqlite3.IntegrityError:
                    response_code = 500
                    query_data = [f"Ошибка - {response_code} (например, база данных недоступна)"]
            else:
                response_code = 500
                query_data = [f"Ошибка - {response_code} (файла базы данных нет)"]

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        return (response_code, query_data)

    def convert_query_data_certain_currency(self, column_names, query_data):
        """
        Метод выполняет преобразование кортежа данных из БД в словарь для вывода его в response
        :param column_names: список названий колонок
        :param query_data: список кортежей с данными
        :return: данные в виде словаря
        """
        if query_data:
            correct_names = {"ID": "id", "FullName": "name", "Code": "code", "Sign": "sign"}
            result = {}
            for i in range(len(column_names)):
                # название колонки из БД
                name_from_db = column_names[i]
                # название ключа для формирования ответа согласно ТЗ
                correct_name = correct_names[name_from_db]
                # записываем данные ключ-значение в словарь
                result[correct_name] = query_data[i]

            return result