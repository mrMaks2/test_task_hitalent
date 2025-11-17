# API сервис Вопросы и Ответы

## Описание

API-сервис для вопросов и ответов, построенный на Django REST Framework с использованием PostgreSQL.

### Модели
*   **Question**: Вопросы с текстом и датой создания
*   **Answer**: Ответы на вопросы с привязкой к пользователю

## Используемые технологии

*   **Python:** Язык программирования.
*   **Django:** HTTP-фреймворк.
*   **PostgreSQL:** База данных.
*   **Docker и Docker Compose:** Для контейнеризации.

## Инструкция по запуску приложения

1.  **Убедитесь, что у вас установлен Docker и Docker Compose.**

2.  **Склонируйте репозиторий:**

    ```bash
    git clone https://github.com/mrMaks2/test_task_hitalent.git
    ```
    
3.  **Создайте файл .env на основе примера.**

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

7.  **Проведение тестов:**

    ```bash
    docker-compose exec web pytest
    ```

### API Endpoints

#### Вопросы
*   **GET /api/v1/questions/** - список всех вопросов с пагинацией.
*   **POST /api/v1/questions/** - создать новый вопрос.
*   **GET /api/v1/questions/{id}/** - получить вопрос со всеми ответами.
*   **DELETE  /api/v1/questions/{id}/** - удалить вопрос (каскадно с ответами).

#### Ответы
*   **POST  /api/v1/questions/{id}/answers/** - добавить ответ к вопросу.
*   **GET  /api/v1/answers/{id}/** - получить конкретный ответ.
*   **DELETE  /api/v1/answers/{id}/** - удалить ответ.
