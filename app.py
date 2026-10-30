from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import urllib.parse


class CustomHandler(SimpleHTTPRequestHandler):

    # Вспомогательный метод для отправки HTML-ответов с нужными заголовками
    def send_html_response(self, status_code, html_content):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(bytes(html_content, 'utf-8'))

    # Обработка GET-запросов
    def do_GET(self):
        try:
            if self.path in ('/', '/contacts'):
                file_path = os.path.join('templates', 'contacts.html')

                with open(file_path, 'r', encoding='utf-8') as file:
                    html_content = file.read()

                # Критерий: возвращается HTML с Content-Type: text/html
                self.send_html_response(200, html_content)
                return

            if self.path.startswith('/static/'):
                return super().do_GET()

            # Ошибка 404
            self.send_error_404()

        except Exception as e:
            # Ошибка 500 при сбое сервера
            print(f"Внутренняя ошибка сервера: {e}")
            self.send_error_500()

    # Критерий: сервер принимает POST-запрос, данные выводятся в консоль без ошибок
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            parsed_data = urllib.parse.parse_qs(post_data)

            print("\n Получены данные из POST-запроса ")
            for key, value in parsed_data.items():
                print(f"{key}: {value[0]}")

            # После успешной отправки перенаправляем обратно на контакты
            self.send_response(303)
            self.send_header('Location', '/contacts')
            self.end_headers()

        except Exception as e:
            print(f"Ошибка при обработке POST: {e}")
            self.send_error_500()

    # Страница 404
    def send_error_404(self):
        html = """
        <!DOCTYPE html>
        <html lang="ru"><head><meta charset="UTF-8"><title>404 - Страница не найдена</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css"></head>
        <body class="bg-light"><div class="container text-center mt-5">
        <h1 class="display-1 text-danger">404</h1><h2>Страница не найдена</h2>
        <a href="/contacts" class="btn btn-primary mt-3">Вернуться к контактам</a>
        </div></body></html>
        """
        self.send_html_response(404, html)

    # Страница 500
    def send_error_500(self):
        html = """
        <!DOCTYPE html>
        <html lang="ru"><head><meta charset="UTF-8"><title>500 - Ошибка сервера</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css"></head>
        <body class="bg-light"><div class="container text-center mt-5">
        <h1 class="display-1 text-warning">500</h1><h2>Внутренняя ошибка сервера</h2>
        <a href="/contacts" class="btn btn-primary mt-3">Попробовать снова</a>
        </div></body></html>
        """
        self.send_html_response(500, html)


def run(server_class=HTTPServer, handler_class=CustomHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Сервер запущен на http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        httpd.server_close()


if __name__ == '__main__':
    run()