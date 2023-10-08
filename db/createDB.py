"""
Этот файл создает базу данных и таблицы в ней
"""

import sqlite3


class CreaterDB:
    """
    Класс отвечает за создание пустых таблиц БД
    Выполняет инициализацию таблиц БС согласно ТЗ
    """

    def init_db(self):
        """
        Создает БД
        Создает две пустые таблицы: Currencies и ExchangeRates
        :return: None
        """
        self.create_db()                    # Создает БД db/database.db
        self.create_db_currencies()         # Создает пустую таблицу: Currencies
        self.create_db_exchange_rates()     # Создает пустую таблицу: ExchangeRates

    def create_db(self):
        """
        Создает БД
        :return: None
        """
        with sqlite3.connect("database.db") as db:
            db.commit()

    def create_db_currencies(self):
        """
        Создает пустую таблицу: Currencies
        :return: None
        """
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            # открываем файл с SQL-запросом на создание таблицы Currencies
            with open("create_db_currencies.txt", "r") as file:
                query = file.read()
            cursor.execute(query)
            db.commit()

    def create_db_exchange_rates(self):
        """
        Создает пустую таблицу: ExchangeRates
        :return: None
        """
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            # открываем файл с SQL-запросом на создание таблицы ExchangeRates
            with open("create_db_exchange_rates.txt", "r") as file:
                query = file.read()
            cursor.execute(query)
            db.commit()


# поскольку к этому классу мы не будем обращаться из вне, то создаем нашу базу данных прямо здесь
if __name__ == "__main__":
    CreaterDB().init_db()