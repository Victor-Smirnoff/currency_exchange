from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from config import Config
from get_performer_currencies import GetPerformerCurrencies
from get_performer_exchange_rates import GetPerformerExchangeRates


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
        Метод обрабаотывает запросы GET
        :return: ответ на запрос
        """
        handler = self.choose_handler()
        response_code, query_data = handler.perform_handling()
        self.send_response(response_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(query_data.encode())

    def choose_handler(self):
        """
        Метод выбирает объект обработчик, который будет отвечать на запрос
        :return: объект класса обработчика
        """
        if self.path == Config.currencies or self.path.startswith(Config.currency):
            handler = GetPerformerCurrencies(self.path)
        if self.path == Config.exchangeRates or self.path.startswith(Config.exchangeRate) or self.path.startswith(Config.exchange):
            handler = GetPerformerExchangeRates(self.path)

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