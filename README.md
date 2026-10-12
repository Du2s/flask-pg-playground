# Flask + PostgreSQL Demo

> 🤖 **Этот README сгенерирован искусственным интеллектом** и предназначен
> исключительно для учебного проекта-заглушки. Не рассматривайте его как
> образец документации для продакшен-проектов.

Учебный проект-заглушка для тренировки автоматизации развёртывания.
Минимальное веб-приложение на Flask, которое подключается к PostgreSQL
и по нажатию кнопок выполняет заранее заданные SQL-запросы, отображая
результат в виде таблицы.

> ⚠️ Проект создан исключительно как песочница для отработки навыков
> CI/CD, контейнеризации, конфигурирования и деплоя. Продакшен-ценности
> не несёт.

---

## Стек

- **Python 3.11+**
- **Flask 3.1** — веб-фреймворк
- **psycopg2 2.9** — драйвер PostgreSQL
- **PostgreSQL 16** — база данных (запускается в Docker)
- **HTML + Vanilla JS** — фронтенд без сборки

---

## Структура проекта

```
.
├── main.py              # Точка входа Flask-приложения
├── sql_request.py       # Класс ReqHandler — обёртка над psycopg2
├── requirements.txt     # Зависимости Python
├── templates/
│   └── index.html       # Единственная страница с кнопками и таблицей
└── README.md
```

---

## Как это работает

1. Пользователь открывает `/` — отдаётся `index.html` с тремя кнопками.
2. Клик по кнопке → JS отправляет `POST /get_data` с `{"button_id": N}`.
3. Flask выполняет соответствующий SQL-запрос через `ReqHandler`.
4. Результат (заголовки + строки) возвращается в JSON.
5. JS рендерит таблицу на странице.

### Соответствие кнопок и запросов

| Кнопка | SQL |
|--------|-----|
| 1 | `SELECT * FROM users;` |
| 2 | `SELECT surname, name, Fname, address FROM users ORDER BY address ASC` |
| 3 | `SELECT surname, name, Fname, exp FROM users WHERE exp > 4;` |

---

## Быстрый старт (локально)

### 1. Поднять PostgreSQL в Docker

```bash
docker run -d \
  --name my-postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16
```

### 2. Создать таблицу и загрузить данные

```bash
docker exec -it my-postgres psql -U myuser -d mydb -c "
CREATE TABLE IF NOT EXISTS users (
  id       serial PRIMARY KEY,
  surname  text,
  name     text,
  Fname    text,
  address  text,
  exp      integer
);"
```

### 3. Установить зависимости Python

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> На Debian/Ubuntu для сборки `psycopg2` нужны `libpq-dev python3-dev build-essential`,
> либо замените пакет на `psycopg2-binary`.

### 4. Запустить приложение

```bash
flask --app main run --debug --host 0.0.0.0 --port 5000
```

Открыть в браузере: <http://localhost:5000>

---

## Конфигурация

Параметры подключения к БД сейчас **захардкожены** в `main.py`:

```python
user_hndlr = ReqHandler("mydb", "myuser", "mysecretpassword", "localhost", "5432")
```

При автоматизации развёртывания это первое, что стоит вынести
в переменные окружения (`.env` + `python-dotenv`), например:

```
DB_NAME=mydb
DB_USER=myuser
DB_PASSWORD=mysecretpassword
DB_HOST=localhost
DB_PORT=5432
```

---

## Что можно потренировать на этом проекте

- 📦 Сборка Docker-образа для самого Flask-приложения
- 🐳 `docker-compose` с двумя сервисами: `app` + `db`
- ⚙️ Вынос конфигурации в переменные окружения
- 🔁 CI/CD: GitHub Actions → сборка → пуш образа → деплой
- 🧪 Health-check-эндпоинт (`/healthz`) и smoke-тесты
- 🗄️ Миграции (Alembic / Flyway) вместо `CREATE TABLE` вручную
- 🔐 Секреты через GitHub Secrets / Vault
- 📊 Логирование и мониторинг

---

## Известные ограничения

- Пароль БД в открытом виде в коде — **только для учебных целей**.
- Нет миграций: схема создаётся вручную.
- Встроенный сервер Flask (`flask run`) не предназначен для продакшена —
  для реального деплоя нужен `gunicorn`/`uwsgi` + reverse-proxy.
- Нет тестов.

---

## Лицензия

MIT — делай что хочешь, но помни: это учебная заглушка.