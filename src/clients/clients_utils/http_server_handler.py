import logging
from http.server import SimpleHTTPRequestHandler
import socketserver
import threading
from socket import SOL_SOCKET, SO_REUSEADDR
import requests


class HTTPServer:

    def __init__(self, port=8090, url='http://localhost'):
        self.port = port
        self.thread = None
        self.httpd = None
        self.run = False
        self.url = url

    def __enter__(self):
        self.start_serve()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_serve()

    def start_serve(self):
        logging.info(F"start http server on {self.url}:{self.port}")
        self.run = True
        self.httpd = socketserver.TCPServer(("", self.port), SimpleHTTPRequestHandler)
        self.httpd.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.thread = threading.Thread(target=self._serve)
        self.thread.start()

    def _serve(self):
        while self.run:
            self.httpd.handle_request()

    def stop_serve(self):
        logging.info(F"stop http server on {self.url}:{self.port}")
        self.run = False
        self.httpd.server_close()


if __name__ == "__main__":
    with HTTPServer() as http_server:
        res = requests.get('http://localhost:8090')
        assert res.status_code == 200
