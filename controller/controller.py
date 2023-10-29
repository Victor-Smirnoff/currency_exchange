import sys
import urllib

sys.path.append('../service')
sys.path.append('../dao')
sys.path.append('../config')
sys.path.append('../dto_response')
sys.path.append('../view')
sys.path.append('../db')

from service import ExchangeService
from dto_response import ErrorResponse
from dao import DaoCurrencyRepository, DaoExchangeRepository
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from config import Config
from view.view import ViewToJSON


class HttpRequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик с реализованными методами:
    do_GET,
    do_POST,
    do_PATCH,
    do_DELETE
    """

    def do_GET(self):
        """
        Метод обрабатывает запросы GET
        :return: ответ на запрос
        """
        if self.path == Config.currencies:                                  # запрос GET /currencies
            response_code, json_data = self.get_currencies()
        elif self.path.startswith(Config.currency):                         # запрос GET /currency/
            response_code, json_data = self.get_currency(self.path)
        elif self.path == Config.exchangeRates:                             # запрос GET /exchangeRates
            response_code, json_data = self.get_exchange_rates()
        elif self.path.startswith(Config.exchangeRate):                     # запрос GET /exchangeRate/
            response_code, json_data = self.get_exchange_rate(self.path)
        elif self.path.startswith(Config.exchange):                         # запрос GET /exchange?
            response_code, json_data = self.get_exchange(self.path)

        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

    def get_currencies(self):
        """
        Метод возвращает данные по запросу GET /currencies
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoCurrencyRepository()
        response = handler.find_all()
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_all_currencies(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def get_currency(self, path):
        """
        Метод возвращает данные по запросу GET /currency/
        :param path: путь запроса
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoCurrencyRepository()
        splitted_path = path.split("/")
        currency_code = splitted_path[-1]
        response = handler.find_by_code(currency_code)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_currency(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def get_exchange_rates(self):
        """
        Метод возвращает данные по запросу GET /exchangeRates
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoExchangeRepository()
        response = handler.find_all()
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_all_exchange_rates(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def get_exchange_rate(self, path):
        """
        Метод возвращает данные по запросу GET /exchangeRate/
        :param path: путь запроса
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        splitted_path = path.split("/")
        currency_codes = splitted_path[-1]
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoExchangeRepository()
        response = handler.find_by_codes(currency_codes)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_exchange_rate(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def get_exchange(self, path):
        """
        Метод возвращает данные по запросу GET /exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT
        :param path: путь запроса
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        args_dict = {}
        cutted_path = path.replace(Config.exchange, "")
        splitted_cutted_path = cutted_path.split("&")
        for arg in splitted_cutted_path:
            key, value = arg.split("=")
            args_dict[key] = value

        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = ExchangeService()
        response = handler.convert_currency(currency_from=args_dict["from"], currency_to=args_dict["to"], amount=args_dict["amount"])
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_exchange(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def do_POST(self):
        """
        Метод обрабатывает запросы POST
        :return: ответ на запрос
        """
        data_dict = self.get_form_fields()

        if self.path == Config.currencies:                                              # запрос POST /currencies
            name, code, sign = data_dict["name"], data_dict["code"], data_dict["sign"]
            response_code, json_data = self.post_currencies(name, code, sign)
        elif self.path == Config.exchangeRates:                                         # запрос POST /exchangeRates
            baseCurrencyCode = data_dict["baseCurrencyCode"]
            targetCurrencyCode = data_dict["targetCurrencyCode"]
            rate = data_dict["rate"]
            response_code, json_data = self.post_exchange_rates(baseCurrencyCode, targetCurrencyCode, rate)

        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

    def get_form_fields(self):
        """
        Метод возвращает словарь с данными полей формы (x-www-form-urlencoded)
        Метод работает для POST и PATCH запросов
        :return: dict с данными, которые были переданы по x-www-form-urlencoded
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data_pieces = post_data.split("&")
        data_dict = {}
        for piece in data_pieces:
            key, value = piece.split("=")
            value = urllib.parse.unquote(value) # Декодируем значение из URL-кодирования, если необходимо
            data_dict[key] = value
        return data_dict

    def post_currencies(self, currency_name, currency_code, currency_sign):
        """
        Метод возвращает данные по запросу POST /currencies
        :param currency_name: Полное имя валюты
        :param currency_code: Код валюты
        :param currency_sign: Символ валюты
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoCurrencyRepository()
        response = handler.save(currency_name, currency_code, currency_sign)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_currency(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def post_exchange_rates(self, baseCurrencyCode, targetCurrencyCode, rate):
        """
        Метод возвращает данные по запросу POST /exchangeRates
        :param baseCurrencyCode: базовая валюта
        :param targetCurrencyCode: целевая валюта
        :param rate: обменный курс
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoExchangeRepository()
        response = handler.save(baseCurrencyCode, targetCurrencyCode, rate)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_exchange_rate(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def do_PATCH(self):
        """
        Метод обрабатывает запросы PATCH
        :return: ответ на запрос
        """
        data_dict = self.get_form_fields()

        if self.path.startswith(Config.exchangeRate):                                   # запрос PATCH /exchangeRate/
            rate = data_dict["rate"]
            splitted_path = self.path.split("/")
            currency_codes = splitted_path[-1]
            response_code, json_data = self.patch_exchange_rate(rate, currency_codes)
        elif self.path.startswith(Config.currencies):                                    # запрос PATCH /currency/
            name, code, sign = data_dict["name"], data_dict["code"], data_dict["sign"]
            response_code, json_data = self.patch_currency(name, code, sign)

        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

    def patch_exchange_rate(self, rate, currency_codes):
        """
        Метод возвращает данные по запросу PATCH /exchangeRate/
        :param rate: обменный курс
        :param currency_codes: коды валют - Валютная пара задаётся идущими подряд кодами валют
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoExchangeRepository()
        response = handler.update(rate, currency_codes)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_exchange_rate(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def patch_currency(self, currency_name, currency_code, currency_sign):
        """
        Метод возвращает данные по запросу PATCH /currency/
        :param currency_name: Полное имя валюты
        :param currency_code: Код валюты
        :param currency_sign: Символ валюты
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoCurrencyRepository()
        response = handler.update(currency_name, currency_code, currency_sign)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_currency(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def do_DELETE(self):
        """
        Метод обрабатывает запросы DELETE
        :return: ответ на запрос
        """
        if self.path.startswith(Config.exchangeRate):                   # запрос DELETE /exchangeRate/
            splitted_path = self.path.split("/")
            currency_codes = splitted_path[-1]
            baseCurrencyCode, targetCurrencyCode = currency_codes[:3], currency_codes[3:]
            response_code, json_data = self.delete_exchange_rate(baseCurrencyCode, targetCurrencyCode)
        elif self.path.startswith(Config.currency):                     # запрос DELETE /currency/
            splitted_path = self.path.split("/")
            currency_code = splitted_path[-1]
            response_code, json_data = self.delete_currency(currency_code)

        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json_data.encode())

    def delete_exchange_rate(self, baseCurrencyCode, targetCurrencyCode):
        """
        Метод возвращает данные по запросу DELETE /exchangeRate/
        :param baseCurrencyCode: код базовой валюты
        :param targetCurrencyCode: код целевой валюты
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoExchangeRepository()
        response = handler.delete(baseCurrencyCode, targetCurrencyCode)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_exchange_rate(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)

    def delete_currency(self, currency_code):
        """
        Метод возвращает данные по запросу DELETE /currency/
        :param currency_code: Код валюты
        :return: кортеж из двух элементов:
        0 - индекс - response_code
        1 - индекс - json_data
        """
        view = ViewToJSON()  # объект класса ViewToJSON для представления
        handler = DaoCurrencyRepository()
        response = handler.delete(currency_code)
        if isinstance(response, ErrorResponse):
            response_code = response.code
            response = {"message": response.message}
            json_data = view.dumps_to_json(response)
        else:
            response_code = 200
            response = view.view_currency(response)
            json_data = view.dumps_to_json(response)
        return (response_code, json_data)


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()



if __name__ == "__main__":
    run(handler_class=HttpRequestHandler)