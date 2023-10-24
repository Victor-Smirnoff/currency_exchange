from dao.DAO_exchange_repository import DaoExchangeRepository
from decimal import Decimal, getcontext
from dto_response.exchange_response import ExchangeResponse
from dto_response.error_response import ErrorResponse
from model.exchange_rate import ExchangeRate
from dao.DAO_currency_repository import DaoCurrencyRepository


class ExchangeService(DaoExchangeRepository):
    """
    Класс для выполнения бизнес-логики получения расчёта перевода определённого количества средств из одной валюты в другую
    """

    def convert_currency(self, currency_from, currency_to, amount):
        """
        Метод принимает в обработку запрос на расчёт перевода определённого количества средств из одной валюты в другую
        :param currency_from: из какой валюты перевод (базовая валюта)
        :param currency_to: в какую валюту перевод (таргет валюта)
        :param amount: количество базовой валюты
        :return: объект класса ExchangeResponse или объект класса ErrorResponse
        """
        # пробуем получить прямой курс и конвертировать
        response = self.get_direct_course(currency_from, currency_to, amount)
        if isinstance(response, ExchangeResponse):
            return response

        # пробуем получить обратный курс и конвертировать
        response = self.get_reverse_course(currency_from, currency_to, amount)
        if isinstance(response, ExchangeResponse):
            return response

        # пробуем получить кросс-курс и конвертировать
        response = self.get_cross_course(currency_from, currency_to, amount)
        if isinstance(response, ExchangeResponse):
            return response

        # если пришли сюда и ничего не вернули, то возвращаем message Обменный курс не найден
        response_code = 404
        message = f"Ошибка {response_code} - Обменный курс {currency_from}-{currency_to} не найден"
        response = ErrorResponse(response_code, message)
        return response

    def get_direct_course(self, currency_from, currency_to, amount):
        getcontext().prec = 7 # устанавливаем точность числа в 7 знаков
        amount = Decimal(amount)
        # складываем коды валют в единую строку для запроса прямого курса
        currency_codes = currency_from + currency_to
        # пробуем получить данные по этому курсу валют
        response = self.find_by_codes(currency_codes)
        if isinstance(response, ExchangeRate):
            DAO_currency_repository = DaoCurrencyRepository()
            base_currency_id = response.BaseCurrencyId
            target_currency_id = response.TargetCurrencyId
            rate = response.Rate
            converted_amount = Decimal(rate) * amount
            converted_amount = str(converted_amount.quantize(Decimal('1.00')))  #  округление до 2 цифр в дробной части
            base_currency = DAO_currency_repository.find_by_id(base_currency_id)
            target_currency = DAO_currency_repository.find_by_id(target_currency_id)
            response = ExchangeResponse(base_currency, target_currency, rate, converted_amount)
            return response
        else:
            return response



