"""
Этот файл добавляет в базу данных в таблицу Currencies несколько валют
Исключительно для тестовых целей!
Не рабочий вариант добавления новых вылют в таблицу Currencies!
Рабочий вариант будет выполнять другой класс!
"""

import sqlite3


class RecorderCurrencies:
    """
    Класс выполняет функцию записи новых строк в базу данных
    """

    def add_currency(self, Code, FullName, Sign):
        """
        Метод добавляет данные в строку таблицы Currencies
        :param Code: Код валюты
        :param FullName: Полное имя валюты
        :param Sign: Символ валюты
        :return: None
        """

        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()
            # открываем файл с SQL-запросом на чтение таблицы Currencies (получение таблицы всех валют)
            with open("add_currency.txt", "r") as file:
                query = file.read()
            try:
                cursor.execute(query, (Code, FullName, Sign))
                db.commit()
            except sqlite3.IntegrityError as e:
                print(f"Ошибка - {e}. Валюта с таким кодом уже существует - 409")


if __name__ == "__main__":
    data = (
        ("RUB", "Russian Ruble", "₽"),
        ("USD", "United States dollar", "$"),
        ("EUR", "Euro", "€"),
        ("AUD", "Australian dollar", "A€"),
        ("GEL", "Georgian Lari", "ლ"),
        ("TRY", "Turkish Lira", "₺")
    )

    recorder = RecorderCurrencies()

    for Code, FullName, Sign in data:
        recorder.add_currency(Code, FullName, Sign)