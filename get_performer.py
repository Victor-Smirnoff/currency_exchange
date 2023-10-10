from performer import Performer
from config import Config


class GetPerformer(Performer):
    """
    Класс принимает в обработку какие-то абстрактные GET запросы
    """
    def __init__(self, path, command="GET"):
        """
        Инициализатор класса GetPerformer
        :param path: путь запроса
        :param command: HTTP метод запроса - GET
        """
        super().__init__(path, command)

    def perform_handling(self):
        """
        Метод выполняет действие над GET запросом
        Вызывает необходимые методы для выполнения данного запроса и возвращает результат
        :return: результат работы функции handler
        индекс 0 - число кода HTTP ответа
        индекс 1 - JSON объект (сериализованный список или словарь с ответом)
        """
        handler, attrs = self.check_path(self.path)
        return self.call_handler(handler, attrs)

    def check_path(self, path):
        """
        Метод проверят путь и возвращает обработчик запроса, который должен быть вызван
        :param path: путь запроса
        :return: возвращает кортеж из двух элементов:
        индекс 0 - функция-обработчик запроса, которая будет определена в дочернем классе, который будет создан для конкретных запросов
        индекс 1 - аргументы для передачи в функцию обработчик (опционально) в виде словаря. если аргументы не требуются, то словарь пуст
        """
        const_paths = {Config.currencies: self.get_all_currencies, Config.exchangeRates: self.get_all_exchange_rates}
        # если путь находится в словаре const_paths, то запрос идет на всю таблицу целиком
        if path in const_paths:
            handler = const_paths[path]
            return handler, {}
        # иначе запрос идет на конкретную строку БД
        else:
            # если путь '/currency/', то запрос идет на конкретную валюту из таблицы currencies
            if path.startswith(Config.currency):
                handler = self.get_certain_currency
                splitted_path = path.split("/")
                currency_code = splitted_path[-1]
                return handler, {"code": currency_code}

            # если путь '/exchangeRate/', то запрос идет на конкретный обменный курс из таблицы exchangeRates
            if path.startswith(Config.exchangeRate):
                handler = self.get_certain_exchange_rate
                splitted_path = path.split("/")
                currency_codes = splitted_path[-1]
                args_dict = {}
                args_dict["currency_codes"] = currency_codes
                return handler, args_dict

            # если путь '/exchange?', то запрос идет на расчёт перевода определённого количества средств
            # из одной валюты в другую. запрос из таблицы exchangeRates и логика выполнения по трём сценариям
            # в отдельном классе будет логика выполнения
            if path.startswith(Config.exchange):
                handler = self.get_currency_exchange
                args_dict = {}
                cutted_path = path.replace(Config.exchange, "")
                splitted_cutted_path = cutted_path.split("&")
                for arg in splitted_cutted_path:
                    key, value = arg.split("=")
                    args_dict[key] = value

                return handler, args_dict

    def call_handler(self, handler, attrs):
        """
        Метод вызывает функцию handler, передает в нее необходимые аргументы
        :param handler: функция handler обработчик запроса
        :param attrs: словарь с атрибутами для обработчика, если пуст, то атрибутов нет
        :return: результат работы функции handler
        """
        if not attrs:
            return handler()
        else:
            if len(attrs) == 1 and "code" in attrs:
                return handler(attrs["code"])
            elif len(attrs) == 1 and "currency_codes" in attrs:
                return handler(currency_codes=attrs["currency_codes"])
            elif len(attrs) == 3:
                return handler(currency_from=attrs["from"], currency_to=attrs["to"], amount=attrs["amount"])

    def raise_NotImplementedError(self):
        raise NotImplementedError

    # имена этих функций приравниваем к имени raise_NotImplementedError чтобы переопределить их в дочерих классах
    get_all_currencies = get_all_exchange_rates = get_certain_currency = get_certain_exchange_rate = get_currency_exchange = raise_NotImplementedError