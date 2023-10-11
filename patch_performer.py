from performer import Performer
from config import Config


class PatchPerformer(Performer):
    """
    Класс принимает в обработку какие-то абстрактные PATCH запросы
    """
    def __init__(self, path, command="PATCH"):
        """
        Инициализатор класса GetPerformer
        :param path: путь запроса
        :param command: HTTP метод запроса - PATCH
        """
        super().__init__(path, command)

    def perform_handling(self, data_dict):
        """
        Метод выполняет действие над PATCH запросом
        Вызывает необходимые методы для выполнения данного запроса и возвращает результат
        :param data_dict: данные поля в запросе в виде словаря
        :return: результат работы функции handler
        индекс 0 - число кода HTTP ответа
        индекс 1 - JSON объект (сериализованный список или словарь с ответом)
        """
        handler, currency_codes = self.check_path(self.path)
        data_dict["currency_codes"] = currency_codes
        return self.call_handler(handler, data_dict)

    def check_path(self, path):
        """
        Метод проверят путь и возвращает обработчик запроса, который должен быть вызван
        :param path: путь запроса
        :return: возвращается функция-обработчик запроса, которая будет определена в дочернем классе
        """
        if self.path.startswith(Config.exchangeRate):
            handler = self.patch_exchange_rates
            splitted_path = path.split("/")
            currency_codes = splitted_path[-1]
            return (handler, currency_codes)

    def call_handler(self, handler, data_dict):
        """
        Метод вызывает функцию handler, передает в нее необходимые аргументы
        :param handler: функция handler обработчик запроса
        :param data_dict: словарь с атрибутами для обработчика
        :return: результат работы функции handler
        """
        # если поля переданы с именем rate и есть добавленный ключ currency_codes
        if "rate" in data_dict and "currency_codes" in data_dict:
            return handler(rate=data_dict["rate"], currency_codes=data_dict["currency_codes"])

    def raise_NotImplementedError(self):
        raise NotImplementedError

    # имена этих функций приравниваем к имени raise_NotImplementedError для того, чтобы переопределить их в дочерних классах
    patch_exchange_rates = raise_NotImplementedError