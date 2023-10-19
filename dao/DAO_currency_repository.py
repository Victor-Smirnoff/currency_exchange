from currency_repository import CurrencyRepository
from model.currency import Currency
from model.error_response import ErrorResponse
import sqlite3
from config.config import Config


class DaoCurrencyRepository(CurrencyRepository):
    """
    Класс для выполнения основных операций в БД над таблицей Currencies
    """
    def find_by_id(self, currency_id):
        """
        Метод для нахождения данных по id
        Получение конкретной валюты
        Это метод Read	SELECT
        :param currency_id: id валюты
        :return: объект с данными из БД
        Это либо объект класса Currency (данные по валюте)
        Либо это объект класса ErrorResponse (код ошибки и сообщение об ошибке)
        """
        try:
            with sqlite3.connect(Config.db_file) as db:
                cursor = db.cursor()

                # открываем файл с SQL-запросом на чтение таблицы Currencies
                with open("../db/GET_currency_from_ID.txt", "r") as file:
                    query = file.read()

                query_data = cursor.execute(query, (currency_id,)).fetchone()

                # если результат SQL-запроса не пуст, то формируем объект класса Currency
                if query_data:
                    # список названий колонок из выполненного SQL-запроса.
                    column_names = [description[0] for description in cursor.description]
                    result = self.get_correct_dict_currency(query_data, column_names)
                    ID, FullName, Code, Sign = result["id"], result["name"], result["code"], result["sign"]
                    query_data = Currency(ID, FullName, Code, Sign)

                # иначе если результат SQL-запроса пуст, то response_code = 404. формируем объект класса ErrorResponse
                else:
                    response_code = 404
                    message = f"Ошибка - Валюта не найдена - {response_code}"
                    query_data = ErrorResponse(response_code, message)

        # иначе если БД недоступна, то response_code = 500. формируем объект класса ErrorResponse
        except sqlite3.IntegrityError:
            response_code = 500
            message = f"Ошибка - {response_code} (база данных недоступна)"
            query_data = ErrorResponse(response_code, message)

        return query_data

    def find_by_code(self, code):
        """
        Метод для нахождения данных по code
        Получение конкретной валюты
        Это метод Read	SELECT
        :param code: код валюты
        :return: объект с данными из БД
        Это либо объект класса Currency (данные по валюте)
        Либо это объект класса ErrorResponse (код ошибки и сообщение об ошибке)
        """
        if not code:
            response_code = 400
            message = f"Ошибка - Код валюты отсутствует в адресе - {response_code}"
            query_data = ErrorResponse(response_code, message)
        else:
            try:
                with sqlite3.connect(Config.db_file) as db:
                    cursor = db.cursor()

                    # открываем файл с SQL-запросом на чтение таблицы Currencies
                    with open("../db/GET_currency.txt", "r") as file:
                        query = file.read()

                    query_data = cursor.execute(query, (code,)).fetchone()

                    # если результат SQL-запроса не пуст, то формируем объект класса Currency
                    if query_data:
                        # список названий колонок из выполненного SQL-запроса.
                        column_names = [description[0] for description in cursor.description]
                        result = self.get_correct_dict_currency(query_data, column_names)
                        ID, FullName, Code, Sign = result["id"], result["name"], result["code"], result["sign"]
                        query_data = Currency(ID, FullName, Code, Sign)

                    # иначе если результат SQL-запроса пуст, то response_code = 404. формируем объект класса ErrorResponse
                    else:
                        response_code = 404
                        message = f"Ошибка - Валюта не найдена - {response_code}"
                        query_data = ErrorResponse(response_code, message)

            # иначе если БД недоступна, то response_code = 500. формируем объект класса ErrorResponse
            except sqlite3.IntegrityError:
                response_code = 500
                message = f"Ошибка - {response_code} (база данных недоступна)"
                query_data = ErrorResponse(response_code, message)

        return query_data

    def get_correct_dict_currency(self, query_data, column_names):
        """
        Метод для получения словаря с данными по конкретной валюте
        :param query_data: результат SQL запроса
        :param column_names: названия колонок в SQL-таблице
        :return: словарь с данными
        """
        correct_names = {"ID": "id", "FullName": "name", "Code": "code", "Sign": "sign"}
        result = {}
        for i in range(len(column_names)):
            name_from_db = column_names[i]  # название колонки из БД
            correct_name = correct_names[name_from_db]  # название ключа для формирования ответа согласно ТЗ
            result[correct_name] = query_data[i]  # записываем данные ключ-значение в словарь
        return result

    def find_all(self):
        """
        Метод возвращает список объектов класса Currency
        :return: list
        """
        try:
            with sqlite3.connect(Config.db_file) as db:
                cursor = db.cursor()

                # открываем файл с SQL-запросом на чтение таблицы Currencies (получение таблицы всех валют)
                with open("../db/GET_currencies.txt", "r") as file:
                    query = file.read()

                query_data_tmp = cursor.execute(query).fetchall()
                query_data = []
                # список названий колонок из выполненного SQL-запроса
                column_names = [description[0] for description in cursor.description]
                for data in query_data_tmp:
                    result = self.get_correct_dict_currency(data, column_names)
                    ID, FullName, Code, Sign = result["id"], result["name"], result["code"], result["sign"]
                    query_data.append(Currency(ID, FullName, Code, Sign))

        except sqlite3.IntegrityError:
            response_code = 500
            message = f"Ошибка - {response_code} (база данных недоступна)"
            query_data = ErrorResponse(response_code, message)

        return query_data