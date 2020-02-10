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
  "message": "Moscow",
  "error": null,
  "data": {
    "coord": {
      "lon": 37.62,
      "lat": 55.75
    },
    "weather": [
      {
        "id": 600,
        "main": "Snow",
        "description": "light snow",
        "icon": "13n"
      }
    ],
    "base": "stations",
    "main": {
      "temp": 271.63,
      "feels_like": 264.28,
      "temp_min": 270.93,
      "temp_max": 272.59,
      "pressure": 994,
      "humidity": 86
    },
    "visibility": 4000,
    "wind": {
      "speed": 7,
      "deg": 200
    },
    "clouds": {
      "all": 90
    },
    "dt": 1581373955,
    "sys": {
      "type": 1,
      "id": 9029,
      "country": "RU",
      "sunrise": 1581397487,
      "sunset": 1581430972
    },
    "timezone": 10800,
    "id": 524901,
    "name": "Moscow",
    "cod": 200
  },
  "meta": {
    "shown": 1
  },
  "time": 228.762
}
```

Ошибка в названии города: 
```bash
curl localhost:8000/v1/weather/wrong-city
```
```json
{
  "message": "city not found",
  "error": null,
  "data": {
    "cod": "404",
    "message": "city not found"
  },
  "meta": {
    "shown": 1
  },
  "time": 224.333
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
