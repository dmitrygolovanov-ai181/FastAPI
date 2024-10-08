### Описание проекта

Это простая реализация API для трекера задач по типу Trello или Jira, построенная с использованием FastAPI. Приложение поддерживает создание, редактирование, удаление задач, а также авторизацию на основе ролей (администратор и пользователь). Приложение отправляет email (mock-функция) ответственному лицу при изменении статуса задачи.

### Функционал
- Создание, редактирование и удаление задач.
- Поддержка статусов задач (TODO, In progress, Done).
- Поддержка авторизации через JWT и ролей (администратор, пользователь).
- Отправка email ответственному лицу при изменении статуса задачи.

### Технологии
- FastAPI
- Pydantic
- SQLAlchemy (если хотите добавить базу данных)
- OAuth2 с JWT-токенами
- passlib для хеширования паролей

---

## Локальный запуск
1)Качайте файлы с гита 
2)В вашей среде Python установите необходимые пакеты, указанные в файле requirements.txt
pip install fastapi uvicorn sqlalchemy pydantic bcrypt passlib python-jose (в терминал)
3) Запуск FastAPI-приложения
Открываете main
Запустите приложение FastAPI с помощью Uvicorn:


uvicorn main:app --reload
Теперь приложение доступно по адресу http://127.0.0.1:8000.

4)Доступ к документации
Перейдите по следующему URL, чтобы использовать автоматически сгенерированную документацию Swagger UI:


http://127.0.0.1:8000/docs
В документации можно протестировать API и создавать запросы прямо из браузера.

5) Авторизация
Для получения токена выполните POST-запрос на маршрут /token, передав username и password (например, admin и adminpass). Используйте полученный токен для доступа к защищенным маршрутам.

Пример запроса для создания задачи

POST /tasks_admin/
Authorization: Bearer <ваш токен>
Body:
{
  "title": "New Task",
  "description": "Test description",
  "responsible_person": "manager@example.com",
  "assignees": ["assignee1@example.com"],
  "status": "TODO",
  "priority": 1
}
