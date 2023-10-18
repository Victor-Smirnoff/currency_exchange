from crud_repository import CrudRepository


class ExchangeRepository(CrudRepository):
    """
    Класс для выполнения основных действий над базой данных в таблице ExchangeRates
    """
    def find_by_codes(self, currency_codes):
        """
        Метод для нахождения данных по currency_codes
        Это метод Read	SELECT
        :param currency_codes: коды валют
        :return: объект с данными из БД
        """
        raise NotImplementedError

    def find_by_codes_with_usd_base(self, currency_code):
        """
        Метод для нахождения данных по code
        Это метод Read	SELECT
        :param currency_code: код валюты для поиска
        :return: объект с данными из БД
        """
        raise NotImplementedError