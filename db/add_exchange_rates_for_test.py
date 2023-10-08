"""
Этот файл добавляет в базу данных в таблицу exchangeRates несколько обменных курсов
Исключительно для тестовых целей!
Не рабочий вариант добавления новых курсов в таблицу exchangeRates!
Рабочий вариант будет выполнять другой класс!
"""

import sqlite3


class RecorderExchangeRates:
    """
    Класс выполняет функцию записи новых строк в базу данных
    """

    def add_exchange_rate(self, BaseCurrencyId, TargetCurrencyId, rate):
        """
        Метод добавляет данные в строку таблицы exchangeRates
        :param BaseCurrencyId: ID базовой валюты - внешний ключ на Currencies.ID
        :param TargetCurrencyId: ID целевой валюты - внешний ключ на Currencies.ID
        :param rate: Курс обмена единицы базовой валюты к единице целевой валюты
        :return: None
        """

        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            # открываем файл с SQL-запросом на чтение таблицы Currencies (получение таблицы всех валют)
            with open("add_exchange_rate.txt", "r") as file:
                query = file.read()
            try:
                cursor.execute(query, (BaseCurrencyId, TargetCurrencyId, rate))
                db.commit()
            except sqlite3.IntegrityError as e:
                print(f"Ошибка - {e}. Валютная пара с таким кодом уже существует - 409")


if __name__ == "__main__":
    data = (
        (2, 3, 0.99),
        (2, 5, 2.67),
        (2, 1, 62.50),
        (5, 1, 22.7)
    )

    recorder = RecorderExchangeRates()

    for BaseCurrencyId, TargetCurrencyId, rate in data:
        recorder.add_exchange_rate(BaseCurrencyId, TargetCurrencyId, rate)