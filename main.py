import json
import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Прочитать данные запроса
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Логика обработки сообщений от Telegram
        data = json.loads(post_data)

        # Токен
        TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
        
        # Приветственные и ошибочные сообщения
        greetings = {
            "ru": "👋 Добро пожаловать! Отправьте ссылку на рилс из Instagram.",
            "en": "👋 Welcome! Send a link to an Instagram reel.",
            "vi": "👋 Chào mừng! Gửi liên kết đến một reel trên Instagram."
        }

        error_messages = {
            "ru": "Не удалось загрузить видео. Проверьте ссылку.",
            "en": "Failed to download the video. Please check the link.",
            "vi": "Không thể tải video. Vui lòng kiểm tra liên kết."
        }

        user_sent_text = {
            "ru": "Видео отправлено пользователем: {user_name}",
            "en": "Video sent by user: {user_name}",
            "vi": "Video được gửi bởi người dùng: {user_name}"
        }

        # Получение данных из запроса
        chat_id = data['message']['chat']['id']
        user_name = data['message']['from']['first_name']
        text = data['message']['text'].strip()

        # Определение языка
        language = "ru"  # по умолчанию русский
        if "instagram.com/reel/" in text:
            language = "en"  # можно добавить логику для автоматического определения языка

        # Приветствие пользователя
        welcome_message = greetings.get(language, "👋 Добро пожаловать!")
        
        # Отправка приветственного сообщения
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': welcome_message
        }

        requests.post(url, data=payload)

        # Обработка видео или ошибок
        if "instagram.com/reel/" in text:
            message = user_sent_text.get(language, "Видео отправлено пользователем: {user_name}")
        else:
            message = error_messages.get(language, "Не удалось загрузить видео. Проверьте ссылку.")
        
        # Ответ на сообщение
        payload['text'] = message.format(user_name=user_name)
        requests.post(url, data=payload)

        # Ответ серверу Telegram
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success"}).encode())

if __name__ == "__main__":
    server_address = ('', 8080)  # Порт по умолчанию для Vercel
    httpd = HTTPServer(server_address, TelegramWebhookHandler)
    print("Server running...")
    httpd.serve_forever()
