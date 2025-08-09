from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Отдаём страницу contacts.html на любой GET
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        try:
            with open("contacts.html", "r", encoding="utf-8") as f:
                html_content = f.read()
            self.wfile.write(html_content.encode("utf-8"))
        except FileNotFoundError:
            self.wfile.write("<h1>Файл contacts.html не найден</h1>".encode("utf-8"))

    def do_POST(self):
        # Получаем длину и читаем данные формы
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)

        # Разбираем данные формы и выводим в консоль
        decoded_data = urllib.parse.parse_qs(post_data.decode("utf-8"))
        print("Получены данные POST-запроса:", decoded_data)

        # Отправляем ответ пользователю
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("<h1>Данные получены! Спасибо.</h1>".encode("utf-8"))

if __name__ == "__main__":
    server_address = ("", 8080)  # localhost:8080
    httpd = HTTPServer(server_address, MyHandler)  # type: ignore
    print("Сервер запущен на http://localhost:8080")
    httpd.serve_forever()
