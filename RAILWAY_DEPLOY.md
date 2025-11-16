# Инструкция по деплою на Railway.com

## Шаг 1: Подготовка проекта

Проект уже подготовлен! Все необходимые файлы созданы:
- ✅ `Procfile` - команда запуска
- ✅ `railway.json` - конфигурация Railway
- ✅ `requirements.txt` - зависимости Python
- ✅ `runtime.txt` - версия Python
- ✅ `release.sh` - скрипт для миграций

## Шаг 2: Создание проекта на Railway

1. Зайдите на [railway.app](https://railway.app)
2. Войдите через GitHub (рекомендуется)
3. Нажмите **"New Project"**
4. Выберите **"Deploy from GitHub repo"**
5. Выберите ваш репозиторий `studyhub`

## Шаг 3: Настройка базы данных

1. В вашем проекте на Railway нажмите **"+ New"**
2. Выберите **"Database"** → **"Add PostgreSQL"**
3. Railway автоматически создаст базу данных и добавит переменную `DATABASE_URL`

## Шаг 4: Настройка переменных окружения

В настройках вашего сервиса (Settings → Variables) добавьте:

```
SECRET_KEY=ваш-секретный-ключ-здесь (сгенерируйте случайную строку)
DEBUG=False
ALLOWED_HOSTS=ваш-домен.railway.app,*.railway.app
```

**Как сгенерировать SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Шаг 5: Настройка деплоя

1. В настройках сервиса найдите раздел **"Deploy"**
2. Убедитесь, что:
   - **Start Command**: `gunicorn backend.wsgi:application` (или оставьте пустым, будет использован Procfile)
   - **Build Command**: оставьте пустым (Railway автоматически установит зависимости)

## Шаг 6: Настройка Release Command (для миграций)

1. В настройках сервиса найдите **"Settings"** → **"Deploy"**
2. В поле **"Release Command"** вставьте:
   ```
   python manage.py migrate --noinput && python manage.py collectstatic --noinput
   ```

## Шаг 7: Деплой

1. Railway автоматически начнет деплой после подключения репозитория
2. Или нажмите **"Deploy"** вручную
3. Дождитесь завершения деплоя
4. Ваше приложение будет доступно по адресу: `ваш-проект.railway.app`

## Шаг 8: Проверка

1. Откройте ваш домен Railway
2. Проверьте, что сайт работает
3. Зайдите в `/admin/` с учетными данными:
   - Username: `admin`
   - Password: `admin123`

## Полезные команды Railway CLI (опционально)

Если установите Railway CLI:
```bash
railway login
railway link
railway up
```

## Решение проблем

- **Ошибка подключения к БД**: Проверьте, что PostgreSQL сервис создан и связан
- **Миграции не выполняются**: Проверьте Release Command
- **Статические файлы не загружаются**: Проверьте, что `collectstatic` выполняется
- **500 ошибка**: Проверьте логи в Railway Dashboard → Logs

