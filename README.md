# Описание
Тестовое задание. REST API для запроса погоды выбранного города.

Сервер запрашивает погоду на сервисе OpenWeatherMap и сохраняет результат в Elasticsearch.

# Подготовка
```bash
git pull https://github.com/pasaranax/weather_test.git
cd weather_test
docker-compose up -d
```
Сервер станет доступен на порту 8000

# Пример использования
Запрос должен происходить методом GET на эндпоинт `/v1/weather/{city}`, где `city` - интересующий нас город.
Ответ будет представлять из себя объект JSON с полями:
- `message` - информация о происходящем
- `error` - информация об ошибке, если есть
- `data` - полезная нагрузка от сервиса погоды

Примеры запросов:

```bash
curl localhost:8000/v1/weather/moscow
```
```json
{
  "message": "Temperature",
  "error": null,
  "data": {
    "temperature": -1.2999999999999545
  },
  "meta": {
    "shown": 1
  },
  "time": 241.374
}
```

Ошибка в названии города: 
```bash
curl localhost:8000/v1/weather/wrong-city
```
```json
{
  "message": null,
  "error": {
    "code": "#error",
    "message": "city not found"
  },
  "data": null,
  "meta": null,
  "time": 267.682
}
```
Неправильно сформированный запрос:
```bash
curl localhost:8000/v1/notweather/
```
```json
{
  "message": null,
  "error": {
    "code": "#method_not_allowed",
    "message": ""
  },
  "data": null,
  "meta": null,
  "time": 1.281
}
```
