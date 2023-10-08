from dataclasses import dataclass


@dataclass
class Config:
    """
    Дата-класс для хранения обрабатываемых путей
    Если в будущем путь поменяется, то менять его будем только тут
    Все остальные классы будут брать эти пути из этого класса
    """

    # ссылка на путь к файлу базы данных
    db_file = "db/database.db"

    # Получение списка валют
    currencies: str = "/currencies"

    # Получение списка всех обменных курсов
    exchangeRates: str = "/exchangeRates"

    # Получение конкретной валюты
    currency: str = "/currency/"

    # Получение конкретного обменного курса
    exchangeRate: str = "/exchangeRate/"

    # Расчёт перевода определённого количества средств из одной валюты в другую
    exchange: str = "/exchange?"