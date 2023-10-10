import sqlite3
import os
from post_performer import PostPerformer
from config import Config


class PostPerformerCurrencies(PostPerformer):
    """
    Класс принимает в обработку POST запросы в таблицу Currencies на добавление новой валюты
    """

    def __init__(self, path, command="POST"):
        """
        Инициализатор класса PostPerformerCurrencies
        :param path: путь запроса
        :param command: HTTP метод запроса - POST
        """
        super().__init__(path, command)

    def post_currencies(self, currency_name, currency_code, currency_sign):
        """
        Метод добавляет новую валюту в таблицу Currencies
        :param currency_name: Полное имя валюты
        :param currency_code: Код валюты
        :param currency_sign: Символ валюты
        :return: кортеж из двух элементов:
        индекс 0 - код HTTP ответа
        индекс 1 - JSON-объект (сериализованный словарь)
        """
        if not currency_name or not currency_code or not currency_sign:
            response_code = 400
            query_data = {"message": f"Отсутствует нужное поле формы - {response_code}"}
        else:
            # проверить наличие файла базы данных перед созданием подключения
            if os.path.exists(Config.db_file):
                try:
                    with sqlite3.connect(Config.db_file) as db:
                        cursor = db.cursor()

                        # открываем файл с SQL-запросом на чтение таблицы Currencies
                        with open("db/POST_currency.txt", "r") as file:
                            query = file.read()

                        try:
                            cursor.execute(query, (currency_name, currency_code, currency_sign))
                            db.commit()
                            response_code = 200
                            with open("db/GET_currency.txt", "r") as file:
                                query = file.read()

                            query_data = cursor.execute(query, (currency_code,)).fetchone()

                            # список названий колонок из выполненного SQL-запроса. это будут преобразованные ключи словаря
                            column_names = [description[0] for description in cursor.description]

                            # теперь необходимо вызвать метод, который преобразует полученные данные в нужный нам словарь
                            query_data = self.convert_query_data_certain_currency(column_names, query_data)

                        except sqlite3.IntegrityError as e:
                            response_code = 409
                            query_data = {"message": f"Ошибка - {e}. Валюта с таким кодом уже существует - 409"}

                except sqlite3.IntegrityError:
                    response_code = 500
                    query_data = {"message": f"Ошибка - {response_code} (база данных недоступна)"}
            else:
                response_code = 500
                query_data = {"message": f"Ошибка - {response_code} (файла базы данных нет)"}

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        return (response_code, query_data)

    def convert_query_data_certain_currency(self, column_names, query_data):
        """
        Метод выполняет преобразование кортежа данных из БД в словарь для вывода его в response
        :param column_names: список названий колонок
        :param query_data: кортеж с данными из БД
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