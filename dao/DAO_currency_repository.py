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
                    correct_names = {"ID": "id", "FullName": "name", "Code": "code", "Sign": "sign"}
                    result = {}
                    for i in range(len(column_names)):
                        name_from_db = column_names[i] # название колонки из БД
                        correct_name = correct_names[name_from_db] # название ключа для формирования ответа согласно ТЗ
                        result[correct_name] = query_data[i] # записываем данные ключ-значение в словарь

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


res = DaoCurrencyRepository()

print(res.find_by_id(1))