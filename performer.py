import json


class Performer:
    """
    Класс выполняет какие-то абстрактные действия
    """
    def __init__(self, path, command=None):
        """
        Инициализатор класса Performer
        :param path: путь запроса
        :param command: HTTP метод запроса (например: 'GET', 'POST', 'PATCH', 'DELETE')
        """
        self.path = path
        self.command = command

    def perform_handling(self):
        """
        Метод выполняет действие над каким-либо запросом
        raise NotImplementedError чтобы в дочерних классах был обязательно переопределен этот метод
        :return:
        """
        raise NotImplementedError

    def dumps_to_json(self, data):
        """
        Метод берет какие-либо данные - словарь или список и преобразует их в JSON-объект
        :param data: словарь или список
        :return: JSON-объект
        """
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        return json_data