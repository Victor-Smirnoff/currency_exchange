from dao.crud_repository import CrudRepository


class CurrencyRepository(CrudRepository):
    """
    Класс для выполнения основных действий над базой данных в таблице Currency
    (добавляется метод для получения данных одной валюты по её коду)
    """
    def find_by_code(self, code):
        """
        Метод для нахождения данных по code
        Это метод Read	SELECT
        :param code: code
        :return: объект с данными из БД
        """
        raise NotImplementedError