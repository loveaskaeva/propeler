# Проект Propeler

Propeler — это современный лендинг + REST API для демонстрации инновационных веб-решений и приёма заявок от клиентов. Разработан в рамках учебного курса.

## Основные возможности

- Адаптивная посадочная страница (HTML/CSS/JS).
- REST API для управления услугами и заявками.
- Сохранение данных в БД (SQLite по умолчанию / PostgreSQL).
- Управление миграциями через Alembic.
- Валидация входных данных (Pydantic).
- Набор автоматических тестов (pytest) с тестовой БД.
- Автодокументация API: `/docs` и `/redoc`.

## Стек технологий

**Frontend**
- **HTML5** — семантическая разметка.
- **CSS3** — стилизация и адаптивная вёрстка.
- **JavaScript (ES6+)** — интерактивность.

**Backend**
- **Python 3.10+** — язык программирования.
- **FastAPI 0.110** — веб-фреймворк для REST API.
- **Uvicorn** — ASGI-сервер.
- **Pydantic v2** — валидация данных.

**База данных и миграции**
- **SQLAlchemy 2.0** — ORM.
- **SQLite** — по умолчанию, для локальной разработки.
- **PostgreSQL** — для продакшена (через `DATABASE_URL`).
- **Alembic** — миграции схемы БД.

**Тестирование**
- **pytest** — фреймворк для тестирования.
- **httpx** — тестовый HTTP-клиент.
- Тестовая БД (отдельный `sqlite` файл, откат после каждого теста).

**Инфраструктура**
- **Git / GitHub** — контроль версий и совместная работа.
- **python-dotenv** — работа с переменными окружения.

## Структура проекта

```text
propeler/
├── app/                    # Бэкенд-приложение
│   ├── __init__.py
│   ├── config.py           # Настройки (pydantic-settings, dotenv)
│   ├── database.py         # SQLAlchemy engine, Base, DI сессии
│   ├── models.py           # ORM-модели (Service, ContactRequest)
│   ├── schemas.py          # Pydantic-схемы запросов/ответов
│   ├── crud.py             # CRUD-операции с БД
│   └── routers/
│       ├── __init__.py
│       ├── services.py     # Эндпоинты /services
│       └── contacts.py     # Эндпоинты /contact-requests
│
├── tests/                  # Автотесты
│   ├── __init__.py
│   ├── conftest.py         # Фикстуры: тестовая БД, TestClient
│   ├── test_services.py    # Тесты эндпоинтов услуг
│   └── test_contacts.py    # Тесты заявок + валидация email
│
├── alembic/                # Миграции Alembic
│   ├── versions/           # Файлы миграций
│   ├── env.py
│   └── script.py.mako
│
├── alembic.ini             # Конфиг Alembic
├── main.py                 # Точка входа: FastAPI app + static/index
├── index.html              # Лендинг (frontend)
├── style.css               # Стили
├── script.js               # Скрипты фронта
├── requirements.txt        # Зависимости Python
├── .env.example            # Пример переменных окружения
├── USER_STORIES.md         # User stories и описание
└── .gitignore
```

**Сущности в БД (2 сущности со связью):**
- `services` — услуги/направления (id, name, description, price, is_active, created_at).
- `contact_requests` — заявки клиентов (id, client_name, email, phone, message, service_id FK → services, created_at).
  Связь: **одна услуга → много заявок** (Foreign Key с каскадным удалением).

## Переменные окружения проекта

Скопируйте `.env.example` в `.env` и при необходимости отредактируйте:

| Переменная       | Описание                                                                        | По умолчанию              |
|------------------|---------------------------------------------------------------------------------|---------------------------|
| `DATABASE_URL`   | URL подключения к БД. SQLite для разработки, PostgreSQL для прода.              | `sqlite:///./propeler.db` |
| `PORT`           | Порт, на котором запускается uvicorn.                                           | `8000`                    |

Пример для PostgreSQL:
```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/propeler
PORT=8000
```

## Как запустить проект

### 1. Клонирование и подготовка

```bash
git clone https://github.com/loveaskaeva/propeler.git
cd propeler
```

### 2. Создать виртуальное окружение и установить зависимости

```bash
py -3 -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 3. Настроить окружение

```bash
copy .env.example .env
```

### 4. Выполнить миграции БД (создаст таблицы)

```bash
alembic upgrade head
```

### 5. Запустить приложение

```bash
py -3 main.py
```

Или через uvicorn явно:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Открыть в браузере:
- Лендинг: `http://localhost:8000/`
- Swagger (документация API): `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### 6. Запустить тесты (проверка работоспособности эндпоинтов)

```bash
pytest tests -v
```

Результат: 5 тестов (3 на services, 2 на contact-requests) должны проходить.

### 7. Полезные команды Alembic

```bash
# Создать новую авто-миграцию по изменениям в models.py
alembic revision --autogenerate -m "описание изменений"

# Применить все миграции до head
alembic upgrade head

# Откатить на 1 миграцию назад
alembic downgrade -1
```

---

## Команда проекта

- **Гусев Матвей**

## API — краткий справочник эндпоинтов

| Метод | Путь                   | Описание                          |
|-------|------------------------|-----------------------------------|
| GET   | `/`                    | Отдаёт `index.html` (лендинг)     |
| GET   | `/services`            | Список услуг (по умолчанию активные) |
| POST  | `/services`            | Создать услугу                   |
| GET   | `/services/{id}`       | Услуга по ID                      |
| PATCH | `/services/{id}`       | Обновить услугу                   |
| GET   | `/contact-requests`    | Список заявок (можно по service_id) |
| POST  | `/contact-requests`    | Создать заявку клиента            |
| GET   | `/docs`                | Swagger UI                        |

---

### User stories и детальное описание — см. [USER_STORIES.md](./USER_STORIES.md).
