# AEZA Promo Monitor

Небольшой мониторинг промо-тарифа AEZA на странице виртуальных серверов.

Скрипт:
- открывает страницу `https://aeza.net/ru/virtual-servers`
- переключает локации по очереди
- ищет тариф `PROMO` в любой доступной локации
- выводит найденные параметры и цену
- умеет работать разово или в режиме постоянного мониторинга

Сейчас точка входа одна: [main.py](/opt/aeza/main.py).

Внутренняя структура:

- [main.py](/opt/aeza/main.py) — CLI entrypoint
- [aeza_monitor/config.py](/opt/aeza/aeza_monitor/config.py) — настройки
- [aeza_monitor/logging_config.py](/opt/aeza/aeza_monitor/logging_config.py) — единый logger проекта
- [aeza_monitor/parser.py](/opt/aeza/aeza_monitor/parser.py) — поиск promo на сайте
- [aeza_monitor/notifier.py](/opt/aeza/aeza_monitor/notifier.py) — консоль и Telegram
- [aeza_monitor/service.py](/opt/aeza/aeza_monitor/service.py) — цикл мониторинга и антиспам-логика
- [aeza_monitor/state.py](/opt/aeza/aeza_monitor/state.py) — хранение состояния в JSON
- [aeza_monitor/models.py](/opt/aeza/aeza_monitor/models.py) — структуры данных

## Зависимости

- Python `3.12.10`
- `uv`
- Playwright
- requests

Установка:

```bash
uv sync
```

Если браузер Playwright ещё не установлен:

```bash
uv run playwright install chromium
```

## Запуск

Разовая проверка:

```bash
uv run python main.py --once
```

Постоянный мониторинг:

```bash
uv run python main.py
```

## Настройки

В [main.py](/opt/aeza/main.py) можно изменить:

- `AEZA_CHECK_INTERVAL` — интервал проверки в секундах
- `AEZA_USE_TELEGRAM` — включение уведомлений
- `AEZA_TELEGRAM_BOT_TOKEN` — токен бота
- `AEZA_TELEGRAM_CHAT_ID` — id чата для уведомлений
- `AEZA_LOG_LEVEL` — уровень логирования
- `AEZA_STATE_FILE` — путь к JSON-файлу состояния

Локальный запуск с переменными окружения:

```bash
AEZA_USE_TELEGRAM=false AEZA_LOG_LEVEL=INFO uv run python main.py --once
```

Шаблон переменных:

```bash
cp .env.example .env
```

Для Docker Compose используется `.env` из корня проекта.

## Как работает поиск Promo

Скрипт не привязан к одной локации. Он проходит по списку доступных локаций и на каждой проверяет, появился ли блок `PROMO`. Если тариф переедет из Стокгольма в другую текущую локацию, монитор всё равно должен его найти.

Ограничение:

- если AEZA полностью изменит структуру страницы, названия локаций или формат карточки тарифа, селекторы и regex-поиск может потребоваться обновить.

## Антиспам Telegram

Для MVP состояние хранится в JSON-файле, путь к которому задаётся через `AEZA_STATE_FILE`.

Типовые варианты:

- локально: `.aeza-monitor-state.json`
- в Docker Compose: `/data/.aeza-monitor-state.json`

Уведомление отправляется только в случаях:

- promo появился после отсутствия
- promo изменился: локация, код плана или цена стали другими
- promo исчез после того, как раньше был найден

Если promo держится без изменений, в Telegram повторное сообщение не уходит.

## Логирование

В проекте один logger `aeza_monitor` на весь проект. Он пишет в stdout, что удобно и для локального запуска, и для Docker.

По умолчанию используется уровень `INFO`.

## Docker Compose

Сборка и запуск:

```bash
cp .env.example .env
docker compose up --build
```

Разовая проверка внутри compose:

```bash
docker compose run --rm aeza-monitor python main.py --once
```

Состояние уведомлений хранится по пути `AEZA_STATE_FILE`. В compose-шаблоне это `/data/.aeza-monitor-state.json`, а каталог `/data` лежит в docker volume `aeza-monitor-data`, поэтому антиспам-логика переживает перезапуск контейнера.

## Тесты

Минимальные тесты покрывают:

- определение событий `promo_found`, `promo_changed`, `promo_lost`, `no_change`
- сохранение и загрузку JSON-состояния

Запуск:

```bash
uv run --group dev pytest
```
