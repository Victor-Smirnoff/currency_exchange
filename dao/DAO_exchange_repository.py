from dao.exchange_repository import ExchangeRepository
from model.exchange_rate import ExchangeRate
from dto_response.error_response import ErrorResponse
import sqlite3
from config import Config


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
                    # SQL-запрос на чтение таблицы ExchangeRates (получение таблицы конкретного курса)
                    query = """SELECT * FROM exchangeRates
                                    WHERE 
                                    BaseCurrencyId = (
                                    SELECT ID as baseCurrency_ID FROM Currencies
                                    WHERE Code == ?
                                    )
                                    AND
                                    TargetCurrencyId = (
                                    SELECT ID as targetCurrency_ID FROM Currencies
                                    WHERE Code == ?
                                    )"""

                    result_data = cursor.execute(query, (baseCurrency, targetCurrency,)).fetchone()

                    # если результат SQL-запроса не пуст, то формируем объект класса ExchangeRate
                    if result_data:
                        ID, BaseCurrencyId, TargetCurrencyId, Rate = result_data[0], result_data[1], result_data[2], result_data[3]
                        query_data = ExchangeRate(ID, BaseCurrencyId, TargetCurrencyId, Rate)

                    # иначе если результат SQL-запроса пуст, то response_code = 404
                    else:
                        response_code = 404
                        message = f"Ошибка - Обменный курс для пары {baseCurrency}-{targetCurrency} не найден - {response_code}"
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
                    # SQL-запрос на чтение таблицы ExchangeRates (получение таблицы конкретного курса)
                    query = """SELECT * FROM exchangeRates
                                    WHERE 
                                    BaseCurrencyId = (
                                    SELECT ID as baseCurrency_ID FROM Currencies
                                    WHERE Code == ?
                                    )
                                    AND
                                    TargetCurrencyId = (
                                    SELECT ID as targetCurrency_ID FROM Currencies
                                    WHERE Code == ?
                                    )"""

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

    def find_all(self):
        """
        Метод для получения списка всех обменных курсов валют из таблицы ExchangeRates
        :return: список с объектами класса ExchangeRate
        """
        try:
            with sqlite3.connect(Config.db_file) as db:
                cursor = db.cursor()
                # SQL-запрос на чтение таблицы Currencies (получение таблицы всех обменных курсов)
                query = """SELECT * FROM exchangeRates"""

                query_data = []
                result_data = cursor.execute(query).fetchall()
                for data in result_data:
                    ID, BaseCurrencyId, TargetCurrencyId, Rate = data[0], data[1], data[2], data[3]
                    exchange_rate_object = ExchangeRate(ID, BaseCurrencyId, TargetCurrencyId, Rate)
                    query_data.append(exchange_rate_object)

        except sqlite3.IntegrityError:
            response_code = 500
            message = f"Ошибка - {response_code} (база данных недоступна)"
            query_data = ErrorResponse(response_code, message)

        return query_data

    def find_by_id(self, id):
        """
        Метод возвращает данные по одному конкретному курсу валют
        Принимает айди обменного курса
        :param id: айди обменного курса
        :return: объект класса ExchangeRate или объект класса ErrorResponse
        """
        try:
            with sqlite3.connect(Config.db_file) as db:
                cursor = db.cursor()
                # SQL-запрос на чтение таблицы ExchangeRates (получение обменного курса по ID)
                query = """SELECT * FROM exchangeRates WHERE ID == ?"""

                data = cursor.execute(query, (id,)).fetchone()

                # если результат SQL-запроса не пуст, то формируем объект класса ExchangeRate
                if data:
                    ID, BaseCurrencyId, TargetCurrencyId, Rate = data[0], data[1], data[2], data[3]
                    query_data = ExchangeRate(ID, BaseCurrencyId, TargetCurrencyId, Rate)

                # иначе если результат SQL-запроса пуст, то response_code = 404
                else:
                    response_code = 404
                    message = f"Ошибка {response_code} - Обменный курс для данного ID <{id}> не найден"
                    query_data = ErrorResponse(response_code, message)

        except sqlite3.IntegrityError:
            response_code = 500
            message = f"Ошибка - {response_code} (база данных недоступна)"
            query_data = ErrorResponse(response_code, message)

        return query_data

    def save(self, baseCurrencyCode, targetCurrencyCode, rate):
        """
        Метод добавляет новый обменный курс в таблицу ExchangeRates
        Это метод Create	INSERT
        :param baseCurrencyCode: базвая валюта
        :param targetCurrencyCode: целевая валюта
        :param rate: обменный курс
        :return: объект класса ExchangeRate если новый обменный курс был добавлен
        или объект класса ErrorResponse если произошла ошибка при записи данных
        """
        currency_codes = baseCurrencyCode + targetCurrencyCode
        # если коды не переданы или длина передаваемой строки не равно 6 символам
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            message = f"Ошибка - {response_code} (Отсутствует нужное поле формы)"
            query_data = ErrorResponse(response_code, message)
        else:
            try:
                with sqlite3.connect(Config.db_file) as db:
                    cursor = db.cursor()

                    # теперь необходимо по коду валюты получить её ID
                    # SQL-запрос на чтение таблицы Currencies (взять ID валюты по её коду)
                    query = """SELECT ID FROM Currencies WHERE Code == ?"""

                    BaseCurrencyId = cursor.execute(query, (baseCurrencyCode,)).fetchone()[0]
                    TargetCurrencyId = cursor.execute(query, (targetCurrencyCode,)).fetchone()[0]

                    # SQL-запрос на чтение таблицы ExchangeRates (добавление нового обменного курса)
                    query = """INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, rate) VALUES(?, ?, ?)"""
                    try:
                        cursor.execute(query, (BaseCurrencyId, TargetCurrencyId, rate))
                        db.commit()
                        query_data = self.find_by_codes(currency_codes)

                    except sqlite3.IntegrityError as e:
                        response_code = 409
                        message = f"Ошибка - {e}. Валютная пара с таким кодом <{baseCurrencyCode}>-<{targetCurrencyCode}> уже существует - 409"
                        query_data = ErrorResponse(response_code, message)

            except sqlite3.IntegrityError:
                response_code = 500
                message = f"Ошибка - {response_code} (база данных недоступна)"
                query_data = ErrorResponse(response_code, message)

        return query_data

    def update(self, rate, currency_codes):
        """Метод выполняет обработку PATCH запроса на обновление данных поля rate в таблице ExchangeRates
        Это метод Update	UPDATE
        :param rate: обменный курс
        :param currency_codes: коды валют - Валютная пара задаётся идущими подряд кодами валют
        :return: объект класса ExchangeRate если обменный курс был изменен
        или объект класса ErrorResponse если произошла ошибка при записи данных
        """
        baseCurrencyCode = currency_codes[:3]
        targetCurrencyCode = currency_codes[3:]
        # если коды не переданы или длина передаваемой строки не равно 6 символам или не передан rate
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            message = f"Ошибка - {response_code} (Отсутствует нужное поле формы - коды валют в адресе запроса {'/exchangeRate/' + currency_codes})"
            query_data = ErrorResponse(response_code, message)
        elif not rate:
            response_code = 400
            message = f"Ошибка - {response_code} (Отсутствует нужное поле формы - 'rate')"
            query_data = ErrorResponse(response_code, message)
        else:
            try:
                with sqlite3.connect(Config.db_file) as db:
                    cursor = db.cursor()

                    # теперь необходимо по коду валюты получить её ID
                    # SQL-запрос на чтение таблицы Currencies (взять ID валюты по её коду)
                    query = """SELECT ID FROM Currencies WHERE Code == ?"""

                    BaseCurrencyId = cursor.execute(query, (baseCurrencyCode,)).fetchone()[0]
                    TargetCurrencyId = cursor.execute(query, (targetCurrencyCode,)).fetchone()[0]

                    # SQL-запрос на чтение для изменения существующего обменного курса таблицы ExchangeRates
                    query = """UPDATE ExchangeRates SET rate = ? WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?"""

                    # пробуем поменять обменный курс
                    cursor.execute(query, (rate, BaseCurrencyId, TargetCurrencyId))
                    db.commit()

                    # если обменный курс был успешно изменён, то получаем данные из таблицы методом self.find_by_codes()
                    query_data = self.find_by_codes(currency_codes)

                    # если тип данных у переменной query_data является ErrorResponse (то есть ошибка)
                    if isinstance(query_data, ErrorResponse):
                        response_code = 404
                        message = f"Ошибка: Валютная пара {baseCurrencyCode}-{targetCurrencyCode} отсутствует в базе данных - {response_code}"
                        query_data = ErrorResponse(response_code, message)

            except sqlite3.IntegrityError:
                response_code = 500
                message = f"Ошибка - {response_code} (база данных недоступна)"
                query_data = ErrorResponse(response_code, message)

        return query_data

    def delete(self, baseCurrencyCode, targetCurrencyCode):
        """
        Метод для удаления обменного курса из таблицы ExchangeRates
        Это метод Delete	DELETE
        :param baseCurrencyCode: код базовой валюты
        :param targetCurrencyCode: код целевой валюты
        :return: объект класса ExchangeRate если обменный курс был удалён
        или объект класса ErrorResponse если произошла ошибка при удалении данных
        """
        currency_codes = baseCurrencyCode + targetCurrencyCode
        # если коды не переданы или длина передаваемой строки не равно 6 символам
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            message = f"Ошибка - {response_code} (Отсутствует нужное поле формы)"
            query_data = ErrorResponse(response_code, message)
        else:
            query_data = self.find_by_codes(currency_codes)
            if isinstance(query_data, ErrorResponse):
                return query_data
            else:
                try:
                    with sqlite3.connect(Config.db_file) as db:
                        cursor = db.cursor()

                        # теперь необходимо по коду валюты получить её ID
                        # SQL-запрос на чтение таблицы Currencies (взять ID валюты по её коду)
                        query = """SELECT ID FROM Currencies WHERE Code == ?"""

                        BaseCurrencyId = cursor.execute(query, (baseCurrencyCode,)).fetchone()[0]
                        TargetCurrencyId = cursor.execute(query, (targetCurrencyCode,)).fetchone()[0]

                        # SQL-запрос на чтение таблицы ExchangeRates (удаление обменного курса)
                        query = """DELETE FROM ExchangeRates WHERE BaseCurrencyId = ? AND TargetCurrencyId = ?"""

                        cursor.execute(query, (BaseCurrencyId, TargetCurrencyId))
                        db.commit()

                except sqlite3.IntegrityError:
                    response_code = 500
                    message = f"Ошибка - {response_code} (база данных недоступна)"
                    query_data = ErrorResponse(response_code, message)

        return query_data