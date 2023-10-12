import sqlite3
import os
from decimal import Decimal, getcontext
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

                    query_data = []
                    result_data = cursor.execute(query).fetchall()

                    for i in range(len(result_data)):
                        one_string_data = []
                        tmp_data = result_data[i]
                        one_string_data.append(tmp_data[0])
                        _, baseCurrency = self.get_certain_currency_for_id(tmp_data[1])
                        _, targetCurrency = self.get_certain_currency_for_id(tmp_data[2])
                        one_string_data.append(baseCurrency)
                        one_string_data.append(targetCurrency)
                        one_string_data.append(tmp_data[3])
                        query_data.append(one_string_data)

                    # теперь необходимо вызвать метод, который преобразует полученные данные в нужный нам список
                    query_data = self.convert_query_data_exchange_rates(query_data)

            except sqlite3.IntegrityError:
                response_code = 500
                query_data = {"message": f"Ошибка - {response_code} (база данных недоступна)"}
        else:
            response_code = 500
            query_data = {"message": f"Ошибка - {response_code} (файла базы данных нет)"}

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        return (response_code, query_data)

    def get_certain_currency_for_id(self, currency_id):
        """
        Метод возвращает данные по одной конкретной валюте (запрос по ID валюты)
        :return: кортеж: код ответа и словарь с данными конкретной валюты из БД
        """
        try:
            with sqlite3.connect(Config.db_file) as db:
                cursor = db.cursor()

                # открываем файл с SQL-запросом на чтение таблицы Currencies
                with open("db/GET_currency_from_ID.txt", "r") as file:
                    query = file.read()

                query_data = cursor.execute(query, (currency_id,)).fetchone()

                # если результат SQL-запроса не пуст, то response_code = 200 и формируем корректный ответ query_data
                if query_data:
                    response_code = 200

                    # список названий колонок из выполненного SQL-запроса. это будут преобразованные ключи словаря
                    column_names = [description[0] for description in cursor.description]

                    # теперь необходимо вызвать метод, который преобразует полученные данные в нужный нам словарь
                    query_data = self.convert_query_data_certain_currency(column_names, query_data)

                # иначе если результат SQL-запроса пуст, то response_code = 404
                else:
                    response_code = 404
                    query_data = {"message": f"Ошибка - Валюта не найдена - {response_code}"}

        except sqlite3.IntegrityError:
            response_code = 500
            query_data = {"message": f"Ошибка - {response_code} (например, база данных недоступна)"}

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

    def convert_query_data_exchange_rates(self, query_data):
        """
        Метод преобразует список списков в список словарей для вывода результата запроса в JSON
        :param query_data: список списков с данными
        :return: список словарей
        """
        result = []
        correct_names = {0: "id", 1: "baseCurrency", 2: "targetCurrency", 3: "rate"}
        for i in range(len(query_data)):
            res_tmp = {}
            for j in range(len(query_data[i])):
                res_tmp[correct_names[j]] = query_data[i][j]
            result.append(res_tmp)

        return result

    def get_certain_exchange_rate(self, currency_codes):
        """
        Метод возвращает данные по одному конкретному курсу валют
        Принимает строку с идущими подряд кодами валют в адресе запроса
        :return: кортеж из двух элементов
        индекс 0 - код HTTP ответа
        индекс 1 - данные ответа
        """
        # если коды не переданы или длина передаваемой строки не равно 6 символам
        if not currency_codes or len(currency_codes) != 6:
            response_code = 400
            query_data = {"message": f"Ошибка - {response_code} (Коды валют пары отсутствуют в адресе или длина двух кодов валют не равна 6)"}
        else:
            baseCurrency = currency_codes[:3]
            targetCurrency = currency_codes[3:]

            # проверить наличие файла базы данных перед созданием подключения
            if os.path.exists(Config.db_file):
                try:
                    with sqlite3.connect(Config.db_file) as db:
                        cursor = db.cursor()

                        # открываем файл с SQL-запросом на чтение таблицы Currencies (получение таблицы всех валют)
                        with open("db/GET_exchange_rate.txt", "r") as file:
                            query = file.read()

                        result_data = cursor.execute(query, (baseCurrency, targetCurrency,)).fetchone()

                        # если результат SQL-запроса не пуст, то response_code = 200 и формируем корректный ответ query_data
                        if result_data:
                            response_code = 200

                            query_data = []
                            query_data.append(result_data[0])
                            _, baseCurrency = self.get_certain_currency_for_id(result_data[1])
                            _, targetCurrency = self.get_certain_currency_for_id(result_data[2])
                            query_data.append(baseCurrency)
                            query_data.append(targetCurrency)
                            query_data.append(result_data[3])

                            # теперь необходимо вызвать метод, который преобразует полученные данные в нужный нам словарь
                            query_data = self.convert_query_data_certain_exchange_rate(query_data)

                        # иначе если результат SQL-запроса пуст, то response_code = 404
                        else:
                            response_code = 404
                            query_data = {"message": f"Ошибка - Обменный курс для пары не найден - {response_code}"}

                except sqlite3.IntegrityError:
                    response_code = 500
                    query_data = {"message": f"Ошибка - {response_code} (база данных недоступна)"}
            else:
                response_code = 500
                query_data = {"message": f"Ошибка - {response_code} (файла базы данных нет)"}

        # запишем данные из коллекции query_data в JSON-объект
        query_data = self.dumps_to_json(query_data)

        return (response_code, query_data)

    def convert_query_data_certain_exchange_rate(self, query_data):
        """
        Метод преобразует список списков в список словарей для вывода результата запроса в JSON
        :param query_data: список списков с данными
        :return: словарь с данными по конкретному обменному курсу
        """
        result = {}
        correct_names = {0: "id", 1: "baseCurrency", 2: "targetCurrency", 3: "rate"}
        for i in range(len(correct_names)):
            result[correct_names[i]] = query_data[i]

        return result

    def get_currency_exchange(self, currency_from, currency_to, amount):
        """
        Метод принимает в обработку запрос на расчёт перевода определённого количества средств из одной валюты в другую
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (таргет валюта)
        :param amount: количество базовой валюты
        :return: кортеж из двух элементов
        индекс 0 - код HTTP ответа
        индекс 1 - данные ответа
        """
        getcontext().prec = 7 # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)
        # складываем коды валют в единую строку для запроса прямого курса
        currency_codes = currency_from + currency_to
        # пробуем получить данные по этому курсу валют
        response_code, query_data = self.get_certain_exchange_rate(currency_codes)
        # если ответ положительный, то умножаем количество на rate, добавляем это в словарь и возвращаем результат
        if response_code == 200:
            query_data = self.loads_from_json(query_data)
            query_data["amount"] = str(amount)
            convertedAmount = Decimal(query_data["rate"]) * amount
            query_data["convertedAmount"] = str(convertedAmount.quantize(Decimal('1.00'))) #  округление до 2 цифр в дробной части
            query_data = self.dumps_to_json(query_data)
            return (response_code, query_data)
        else:
            # пробуем взять обратный курс
            reversed_currency_codes = currency_to + currency_from
            # пробуем получить данные по этому курсу валют
            response_code, query_data = self.get_certain_exchange_rate(reversed_currency_codes)
            # если ответ положительный, то умножаем количество на 1/rate, добавляем это в словарь и возвращаем результат
            if response_code == 200:
                query_data = self.loads_from_json(query_data)
                query_data["amount"] = str(amount)
                convertedAmount = (1 / Decimal(query_data["rate"])) * amount
                query_data["convertedAmount"] = str(convertedAmount.quantize(Decimal('1.00'))) #  округление до 2 цифр в дробной части

                # здесь надо ещё поменять местами значения baseCurrency и targetCurrency,
                # потому что в результате выбора обратного курса они поменялись местами
                baseCurrency_data = query_data["targetCurrency"]
                targetCurrency_data = query_data["baseCurrency"]
                query_data["baseCurrency"] = baseCurrency_data
                query_data["targetCurrency"] = targetCurrency_data
                # а также обновить обменный курс, так как берем обратный
                converted_rate = 1 / Decimal(query_data["rate"])
                query_data["rate"] = str(converted_rate.quantize(Decimal('1.000000')))

                query_data = self.dumps_to_json(query_data)
                return (response_code, query_data)

        # если пришли сюда и ничего не вернули, то пробуем пройти по третьему сценарию
        USD_A = "USD" + currency_from
        USD_B = "USD" + currency_to
        response_code_USD_A, query_data_USD_A = self.get_certain_exchange_rate(USD_A)
        response_code_USD_B, query_data_USD_B = self.get_certain_exchange_rate(USD_B)
        # если существуют валютные пары USD-A и USD-B, то считаем кросс курс через USD
        if response_code_USD_A == response_code_USD_B == 200:
            query_data = {}
            query_data_USD_A = self.loads_from_json(query_data_USD_A)
            query_data_USD_B = self.loads_from_json(query_data_USD_B)
            baseCurrency_data = query_data_USD_A["targetCurrency"]
            targetCurrency_data = query_data_USD_B["targetCurrency"]
            query_data["baseCurrency"] = baseCurrency_data
            query_data["targetCurrency"] = targetCurrency_data
            rate = Decimal(query_data_USD_B["rate"]) / Decimal(query_data_USD_A["rate"])
            query_data["amount"] = str(amount)
            query_data["rate"] = str(rate)
            convertedAmount = rate * amount
            query_data["convertedAmount"] = str(convertedAmount.quantize(Decimal('1.00'))) #  округление до 2 цифр в дробной части

            response_code = response_code_USD_A
            query_data = self.dumps_to_json(query_data)
            return (response_code, query_data)

        # если пришли сюда и ничего не вернули, то возвращаем message Валюта не найдена
        response_code = 404
        query_data = {"message": f"Ошибка {response_code} - Обменный курс {currency_from}-{currency_to} не найден"}
        query_data = self.dumps_to_json(query_data)
        return (response_code, query_data)