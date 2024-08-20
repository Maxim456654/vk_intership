Шаги для запуска

1. Клонирование репозитория
``` 
git clone <ссылка-на-репозиторий>
cd <название-проекта>
```
2. Запуск Docker Compose
```
docker-compose up -d
```
   Эта команда запустит API-сервис и Tarantool в контейнерах Docker.
3. Проверка статуса контейнеров
Убедитесь, что контейнеры запущены и работают:
```
docker-compose ps
```
4. Доступ к API
   После успешного запуска, API будет доступен по адресу:
```
http://localhost:5000
```

Полная документация API

1. POST /api/login
   Описание: Этот эндпоинт используется для аутентификации пользователя и получения токена авторизации.
   Пример запроса:
```
curl -X POST http://localhost:5000/api/login \
-H "Content-Type: application/json" \
-d '{"username", "your_username"}'
```
   Пример успешного ответа:
```
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
   Возможные ошибки:
   400 Bad Request: Неверный формат запроса 
```
{
  "message": "Invalid username or password"
}
```
   401 Unauthorized: Неверный username или password.
```
{
    "message": "Invalid username or password"
}
```

2. POST /api/write

   Описание: Этот эндпоинт используется для записи данных пачками в KV-хранилище.
   Пример запроса:
```
curl -X POST http://localhost:5000/api/write \
-H "Authorization: Bearer <ваш_токен>" \
-H "Content-Type: application/json" \
-d '{"key1": "value1", "key2": "value2"}'
```
   Пример успешного ответа:
```
{
  "message": "Data successfully written"
}
```
   Возможные ошибки:
   400 Bad Request: Неверный формат запроса.
```
{
  "message": "Invalid request format"
}
```
   401 Unauthorized: Неверный или отсутствующий токен авторизации.
```
{
  "message": "Unauthorized"
}
```
   500 Internal Server Error: Ошибка на стороне сервера или базы данных.
```
        {
          "message": "Internal Server Error"
        }
```

3. POST /api/read

   Описание: Этот эндпоинт используется для чтения данных пачками из KV-хранилища.
   Пример запроса:
```
curl -X POST http://localhost:5000/api/read \
-H "Authorization: Bearer <ваш_токен>" \
-H "Content-Type: application/json" \
-d '{"keys": ["key1", "key2"]}'
```
   Пример успешного ответа:
```
{
  "key1": "value1",
  "key2": "value2"
}
```
   Возможные ошибки: 
   400 Bad Request: Неверный формат запроса.
```
{
  "message": "Invalid request format"
}
```
   401 Unauthorized: Неверный или отсутствующий токен авторизации.
```
{
  "message": "Unauthorized"
}
```
   404 Not Found: Запрашиваемые ключи не найдены.
```
{
  "message": "Keys not found"
}
```
   500 Internal Server Error: Ошибка на стороне сервера или базы данных.
```
{
  "message": "Internal Server Error"
}
```
