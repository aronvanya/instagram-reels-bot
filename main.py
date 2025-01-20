import json
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Читаем данные из POST запроса
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Парсим данные в JSON
        data = json.loads(post_data)

        # Получаем информацию о сообщении от Telegram
        chat_id = data['message']['chat']['id']
        user_name = data['message']['from']['first_name']
        text = data['message']['text']

        # Отправляем ответ пользователю
        url = f"https://api.telegram.org/bot<твой_токен>/sendMessage"  # Замените на свой токен
        payload = {
            'chat_id': chat_id,
            'text': f"Привет, {user_name}! Ты отправил: {text}"  # Ответ пользователю
        }

        # Отправка сообщения в Telegram
        requests.post(url, data=payload)

        # Ответ на запрос от Telegram (всегда 200)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())

# Запускаем сервер
if __name__ == "__main__":
    server_address = ('', 8080)  # Указываем порт
    httpd = HTTPServer(server_address, TelegramWebhookHandler)  # Создаём сервер
    print("Server running...")
    httpd.serve_forever()  # Запуск сервера
