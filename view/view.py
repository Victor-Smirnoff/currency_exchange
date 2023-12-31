import json

from dao import DaoCurrencyRepository
from model.currency import Currency


class ViewToJSON:
    """
    Класс просто берет коллекцию python и возвращает JSON
    """
    def dumps_to_json(self, data):
        """
        Метод берет какие-либо данные - словарь или список и преобразует их в JSON-объект
        :param data: словарь или список
        :return: JSON-объект
        """
        json_data = json.dumps(data, indent=4, ensure_ascii=False)
        return json_data

    def view_all_currencies(self, response):
        """
        Метод для обработки данных по всем валютам
        :param response: это список всех валют - список объектов класса Currency
        :return: преобразованный список словарей с данными по всем валютам, который потом можно превратить в JSON
        """
        response_to_json = []
        for currency in response:
            currency_dict = {"id": currency.ID, "name": currency.FullName, "code": currency.Code, "sign": currency.Sign}
            response_to_json.append(currency_dict)

        return response_to_json

    def view_currency(self, response):
        """
        Метод для обработки данных по одной валюте
        :param response: объект класса Currency
        :return: словарь с данными о валюте или словарь с ошибкой
        """
        currency_dict = {"id": response.ID, "name": response.FullName, "code": response.Code, "sign": response.Sign}
        return currency_dict

    def view_all_exchange_rates(self, response):
        """
        Метод для обработки данных по всем обменным курсам
        :param response: это список всех обменных курсов - список объектов класса ExchangeRate
        :return: преобразованный список словарей с данными по всем валютам, который потом можно превратить в JSON
        """
        obj_dao_currency = DaoCurrencyRepository() # объект класса DaoCurrencyRepository для поиска валюты по ID
        response_to_json = []
        for exchange_rate in response:
            exchange_rate_id = exchange_rate.ID
            BaseCurrencyId = exchange_rate.BaseCurrencyId
            TargetCurrencyId = exchange_rate.TargetCurrencyId
            Rate = exchange_rate.Rate
            baseCurrency = obj_dao_currency.find_by_id(BaseCurrencyId)
            baseCurrency = self.view_currency(baseCurrency)
            targetCurrency = obj_dao_currency.find_by_id(TargetCurrencyId)
            targetCurrency = self.view_currency(targetCurrency)
            exchange_rate_dict = {"id": exchange_rate_id,
                                  "baseCurrency": baseCurrency,
                                  "targetCurrency": targetCurrency,
                                  "rate": Rate}
            response_to_json.append(exchange_rate_dict)

        return response_to_json

    def view_exchange_rate(self, response):
        """
        Метод для обработки данных по одному конкретному обменному курсу
        :param response: это объект класса ExchangeRate
        :return: преобразованный словарь с данными по конкретному обменному курсу, который потом можно превратить в JSON
        """
        obj_dao_currency = DaoCurrencyRepository()  # объект класса DaoCurrencyRepository для поиска валюты по ID
        exchange_rate_id = response.ID
        BaseCurrencyId = response.BaseCurrencyId
        TargetCurrencyId = response.TargetCurrencyId
        Rate = response.Rate
        baseCurrency = obj_dao_currency.find_by_id(BaseCurrencyId)
        baseCurrency = self.view_currency(baseCurrency)
        targetCurrency = obj_dao_currency.find_by_id(TargetCurrencyId)
        targetCurrency = self.view_currency(targetCurrency)
        response_to_json = {"id": exchange_rate_id,
                              "baseCurrency": baseCurrency,
                              "targetCurrency": targetCurrency,
                              "rate": Rate}
        return response_to_json

    def view_exchange(self, response):
        """
        Метод для обработки данных по расчёту перевода определённого количества средств из одной валюты в другую
        :param response: это объект класса ExchangeResponse
        :return: преобразованный словарь с данными по обмену валют, который потом можно превратить в JSON
        """
        base_currency = response.baseCurrency
        target_currency = response.targetCurrency
        rate = response.rate
        amount = response.amount
        converted_amount = response.convertedAmount
        response_to_json = {"baseCurrency": self.view_currency(base_currency),
                            "targetCurrency": self.view_currency(target_currency),
                            "rate": rate,
                            "amount": amount,
                            "convertedAmount": converted_amount
                            }
        return response_to_json