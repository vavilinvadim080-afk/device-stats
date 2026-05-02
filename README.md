# Device Statistics Service

REST API сервис для сбора и анализа данных, поступающих с устройств.

## Описание

Сервис принимает показания `{x, y, z}` от устройств по их идентификатору, сохраняет в базу данных с временной меткой и предоставляет аналитику (min, max, count, sum, median) за всё время или за указанный период.

## Стек

| Технология | Роль |
|---|---|
| Python 3.11 | Язык разработки |
| FastAPI | Веб-фреймворк |
| SQLAlchemy | ORM (работа с БД) |
| SQLite | База данных |
| Uvicorn | ASGI-сервер |
| Docker + docker-compose | Контейнеризация |

## Запуск

### Локально (без Docker)

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Сервис доступен на http://localhost:8000

Автодокументация: http://localhost:8000/docs

### Через Docker

```bash
docker-compose up --build
```

## API

### Принять данные с устройства

```
POST /devices/{device_id}/data
```

**Тело запроса:**
```json
{"x": 1.5, "y": 2.3, "z": 0.8}
```

**Ответ (201 Created):**
```json
{
  "id": 1,
  "device_id": "sensor_42",
  "x": 1.5,
  "y": 2.3,
  "z": 0.8,
  "timestamp": "2024-05-01T10:00:00"
}
```

### Получить аналитику по устройству

```
GET /devices/{device_id}/analytics
GET /devices/{device_id}/analytics?from_ts=2024-01-01T00:00:00&to_ts=2024-12-31T23:59:59
```

**Ответ (200 OK):**
```json
{
  "device_id": "sensor_42",
  "period_from": null,
  "period_to": null,
  "x": {"min": 1.5, "max": 5.5, "count": 3, "sum": 10.0, "median": 3.0},
  "y": {"min": 1.1, "max": 4.0, "count": 3, "sum": 7.4, "median": 2.3},
  "z": {"min": 0.8, "max": 3.3, "count": 3, "sum": 5.6, "median": 1.5}
}
```

## Примеры curl

```bash
# Отправить данные
curl -X POST http://localhost:8000/devices/sensor_1/data \
  -H "Content-Type: application/json" \
  -d '{"x": 1.5, "y": 2.3, "z": 0.8}'

# Получить аналитику за всё время
curl http://localhost:8000/devices/sensor_1/analytics

# Аналитика за период
curl "http://localhost:8000/devices/sensor_1/analytics?from_ts=2024-01-01T00:00:00&to_ts=2024-12-31T23:59:59"
```
