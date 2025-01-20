FROM python:3.9-slim

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean

# Установка рабочего каталога
WORKDIR /app

# Копирование файлов
COPY . .

# Установка Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["python", "main.py"]
