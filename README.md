# Chat API - Django REST Framework

REST API для управления чатами и сообщениями.

## Технологии

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose

## Функциональность

1. **Создание чата**
   - `POST /api/chats/`
   - Тело: `{"title": "Название чата"}`

2. **Отправка сообщения**
   - `POST /api/chats/{id}/messages/`
   - Тело: `{"text": "Текст сообщения"}`

3. **Получение чата с сообщениями**
   - `GET /api/chats/{id}?limit=20`
   - Параметр `limit` (по умолчанию 20, максимум 100)

4. **Удаление чата**
   - `DELETE /api/chats/{id}`
   - Удаляет чат и все связанные сообщения (каскадное удаление)

## Валидация

- Название чата: 1-200 символов
- Текст сообщения: 1-5000 символов
- Пробелы по краям автоматически обрезаются

## Запуск проекта

1.  **Убедитесь, что у вас установлен Docker и Docker Compose.**

2.  **Склонируйте репозиторий:**

    ```bash
    git clone https://github.com/mrMaks2/test_task_hitalent.git
    cd test_task_hitalent
    ```

3.  **Создайте файл .env по примеру .env.example в корне проекта с данными для settings и PostgerSQL:**

    ```bash
    cp .env.example .env
    ```

4.  **Запустите проект с помощью команды:**

    ```bash
    docker-compose up --build
    ```

5.  **После запуска контейнеров, выполните миграции для применения изменений в базе данных:**

    ```bash
    docker-compose exec web python manage.py migrate
    ```

6.  **Создание суперпользователя:**

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

7.  **Тестирование:**

    ```bash
    docker-compose exec web pytest
    ```