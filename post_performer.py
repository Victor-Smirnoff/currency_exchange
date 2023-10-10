from performer import Performer
from config import Config


class PostPerformer(Performer):
    """
    Класс принимает в обработку какие-то абстрактные POST запросы
    """
    def __init__(self, path, command="POST"):
        """
        Инициализатор класса GetPerformer
        :param path: путь запроса
        :param command: HTTP метод запроса - POST
        """
        super().__init__(path, command)

    def perform_handling(self, data_dict):
        """
        Метод выполняет действие над POST запросом
        Вызывает необходимые методы для выполнения данного запроса и возвращает результат
        :param data_dict: данные поля в запросе в виде словаря
        :return: результат работы функции handler
        индекс 0 - число кода HTTP ответа
        индекс 1 - JSON объект (сериализованный список или словарь с ответом)
        """
        handler = self.check_path(self.path)
        return self.call_handler(handler, data_dict)

    def check_path(self, path):
        """
        Метод проверят путь и возвращает обработчик запроса, который должен быть вызван
        :param path: путь запроса
        :return: возвращается функция-обработчик запроса, которая будет определена в дочернем классе
        """
        const_paths = {Config.currencies: self.post_currencies, Config.exchangeRates: self.post_exchange_rates}
        # если путь находится в словаре const_paths, то запрос идет на всю таблицу целиком
        if path in const_paths:
            handler = const_paths[path]
            return handler

    def call_handler(self, handler, data_dict):
        """
        Метод вызывает функцию handler, передает в нее необходимые аргументы
        :param handler: функция handler обработчик запроса
        :param data_dict: словарь с атрибутами для обработчика
        :return: результат работы функции handler
        """
        # если поля переданы с именами name, code и sign, то вызываем функцию post_currencies(name, code, sign)
        if "name" in data_dict and "code" in data_dict and "sign" in data_dict:
            return handler(currency_name=data_dict["name"], currency_code=data_dict["code"], currency_sign=data_dict["sign"])
        # если поля переданы с именами baseCurrencyCode, targetCurrencyCode, rate, то вызываем функцию post_currencies(name, code, sign)
        if "baseCurrencyCode" in data_dict and "targetCurrencyCode" in data_dict and "rate" in data_dict:
            return handler(baseCurrencyCode=data_dict["baseCurrencyCode"], targetCurrencyCode=data_dict["targetCurrencyCode"], rate=data_dict["rate"])

    def raise_NotImplementedError(self):
        raise NotImplementedError

    # имена этих функций приравниваем к имени raise_NotImplementedError для того, чтобы переопределить их в дочерних классах
    post_currencies = post_exchange_rates = raise_NotImplementedError