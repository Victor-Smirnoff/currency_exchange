from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import urllib.parse
from config import Config
from get_performer_currencies import GetPerformerCurrencies
from get_performer_exchange_rates import GetPerformerExchangeRates
from post_performer_currencies import PostPerformerCurrencies


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
        handler = self.choose_get_handler()
        response_code, query_data = handler.perform_handling()
        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(query_data.encode())

    def choose_get_handler(self):
        """
        Метод выбирает объект обработчик, который будет отвечать на запрос
        :return: объект класса обработчика
        """
        if self.path == Config.currencies or self.path.startswith(Config.currency):
            handler = GetPerformerCurrencies(self.path)
        if self.path == Config.exchangeRates or self.path.startswith(Config.exchangeRate) or self.path.startswith(Config.exchange):
            handler = GetPerformerExchangeRates(self.path)

        return handler

    def do_POST(self):
        """
        Метод обрабатывает запросы POST
        :return: ответ на запрос
        """
        data_dict = self.get_form_fields()
        handler = self.choose_post_handler(data_dict)
        response_code, query_data = handler.perform_handling(data_dict)

    def get_form_fields(self):
        """
        Метод возвращает словарь с данными полей формы (x-www-form-urlencoded)
        :return: dict с данными, которые были переданы по x-www-form-urlencoded
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data_pieces = post_data.split("&")
        data_dict = {}
        for piece in data_pieces:
            key, value = piece.split("=")
            # Декодируем значение из URL-кодирования, если необходимо
            value = urllib.parse.unquote(value)
            data_dict[key] = value

        return data_dict

    def choose_post_handler(self, data_dict):
        """
        Метод выбирает обработчик в зависимости от пути запроса
        :return: объект класса обработчика
        """
        if self.path == Config.currencies:
            handler = PostPerformerCurrencies(self.path)
        # if self.path == Config.exchangeRates:
        #     handler = PostPerformerExchangeRates(self.path)

        return handler





def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()



if __name__ == "__main__":
    run(handler_class=HttpRequestHandler)