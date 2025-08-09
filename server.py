from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Любой GET-запрос — отдаём contacts.html (страницу Контакты)
            filename = "contacts.html"  # Переименуйте свой файл с HTML в contacts.html или укажите нужное имя

            with open(filename, "r", encoding="utf-8") as f:
                html_content = f.read()

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
            logging.info(f"Отправлена страница {filename} на GET-запрос {self.path}")

        except FileNotFoundError:
            self.send_error(404, "Файл не найден")
        except Exception as e:
            logging.error(f"Ошибка при обработке GET-запроса: {e}")
            self.send_error(500, "Внутренняя ошибка сервера")

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            decoded_data = urllib.parse.parse_qs(post_data.decode("utf-8"))
            logging.info(f"Получены данные POST-запроса: {decoded_data}")

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>Данные получены! Спасибо.</h1>".encode("utf-8"))

        except Exception as e:
            logging.error(f"Ошибка при обработке POST-запроса: {e}")
            self.send_error(500, "Внутренняя ошибка сервера")


if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, MyHandler)  # type: ignore
    logging.info("Сервер запущен на http://localhost:8080")
    httpd.serve_forever()
