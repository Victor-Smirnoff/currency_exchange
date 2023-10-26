import sys

from service.exchange_service import ExchangeService

sys.path.append('../dao')
sys.path.append('../config')
sys.path.append('../dto_response')
sys.path.append('../view')
sys.path.append('../db')

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
        if self.path == Config.currencies:                                  # запрос в GET /currencies
            response_code, json_data = self.get_currencies()
        elif self.path.startswith(Config.currency):                         # запрос в GET /currency/
            response_code, json_data = self.get_currency(self.path)
        elif self.path == Config.exchangeRates:                             # запрос в GET /exchangeRates
            response_code, json_data = self.get_exchange_rates()
        elif self.path.startswith(Config.exchangeRate):                     # запрос в GET /exchangeRate/
            response_code, json_data = self.get_exchange_rate(self.path)
        elif self.path.startswith(Config.exchange):                         # запрос в GET /exchange?
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



    # def do_POST(self):
    #     """
    #     Метод обрабатывает запросы POST
    #     :return: ответ на запрос
    #     """
    #     data_dict = self.get_form_fields()
    #     handler = self.choose_post_handler()
    #     response_code, query_data = handler.perform_handling(data_dict)
    #     self.send_response(response_code)
    #     self.send_header('Content-type', 'application/json')
    #     self.end_headers()
    #     self.wfile.write(query_data.encode())
    #
    # def get_form_fields(self):
    #     """
    #     Метод возвращает словарь с данными полей формы (x-www-form-urlencoded)
    #     :return: dict с данными, которые были переданы по x-www-form-urlencoded
    #     """
    #     content_length = int(self.headers['Content-Length'])
    #     post_data = self.rfile.read(content_length).decode('utf-8')
    #     data_pieces = post_data.split("&")
    #     data_dict = {}
    #     for piece in data_pieces:
    #         key, value = piece.split("=")
    #         # Декодируем значение из URL-кодирования, если необходимо
    #         value = urllib.parse.unquote(value)
    #         data_dict[key] = value
    #
    #     return data_dict
    #
    # def choose_post_handler(self):
    #     """
    #     Метод выбирает обработчик в зависимости от пути запроса
    #     :return: объект класса обработчика
    #     """
    #     if self.path == Config.currencies:
    #         handler = PostPerformerCurrencies(self.path)
    #     if self.path == Config.exchangeRates:
    #         handler = PostPerformerExchangeRates(self.path)
    #
    #     return handler
    #
    # def do_PATCH(self):
    #     """
    #     Метод обрабатывает запросы PATCH
    #     :return: ответ на запрос
    #     """
    #     data_dict = self.get_form_fields()
    #     handler = self.choose_patch_handler()
    #     response_code, query_data = handler.perform_handling(data_dict)
    #     self.send_response(response_code)
    #     self.send_header('Content-type', 'application/json')
    #     self.end_headers()
    #     self.wfile.write(query_data.encode())
    #
    # def choose_patch_handler(self):
    #     """
    #     Метод выбирает обработчик PATCH запроса
    #     :return: функция обработчик
    #     """
    #     if self.path.startswith(Config.exchangeRate):
    #         handler = PatchPerformerExchangeRates(self.path)
    #
    #     return handler




def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()



if __name__ == "__main__":
    run(handler_class=HttpRequestHandler)