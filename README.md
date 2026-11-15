# Learning Log

Работающий сайт: https://learning-log-rksi.vercel.app/
Админка: https://learning-log-rksi.vercel.app/admin/

Развёрнут в отдельном проекте Vercel `learning-log-rksi`, данные хранятся в отдельной PostgreSQL-базе Neon `learning-log-rksi-db`. Пароль администратора передаётся владельцу отдельно.


Учебный дневник на Python 3.12 и Django 5.2: регистрация, темы, записи, редактирование и личные данные каждого пользователя. Админка: `/admin/`.

## Локальный запуск (PowerShell)

```powershell
py -3.12 -m venv ll_env
.\ll_env\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# В .env установите DJANGO_DEBUG=True для разработки и собственный DJANGO_SECRET_KEY.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте http://127.0.0.1:8000/. В Linux/macOS используйте `python3.12 -m venv ll_env` и `source ll_env/bin/activate`.

## Настройки окружения

`.env` читается локально автоматически, а Docker Compose передаёт его контейнеру. Секреты не коммитить.

| Переменная | Назначение |
| --- | --- |
| DJANGO_SECRET_KEY | Собственный длинный случайный ключ; обязателен при DEBUG=False |
| DJANGO_DEBUG | True локально, False на сервере |
| DJANGO_ALLOWED_HOSTS | Разрешённые имена/IP через запятую без схемы и порта |
| DJANGO_CSRF_TRUSTED_ORIGINS | Полные доверенные адреса со схемой и портом |
| DJANGO_USE_HTTPS | True на Vercel/HTTPS; False при прямом HTTP учебного сервера |
| SQLITE_PATH | Локальный путь SQLite; Compose задаёт /app/data/db.sqlite3 |
| DATABASE_URL | PostgreSQL URL для Vercel; имеет приоритет над SQLite, требует TLS |
| APP_BIND_IP | 127.0.0.1 локально; 0.0.0.0 на учебном сервере |
| APP_PORT | Порт, выделенный преподавателем |

## Docker / учебный сервер

Создайте `.env` из примера. Укажите секрет, DEBUG=False, IP сервера в ALLOWED_HOSTS, полный HTTP-адрес с выделенным портом в CSRF_TRUSTED_ORIGINS, APP_BIND_IP=0.0.0.0 и APP_PORT.

```sh
docker compose up -d --build
docker compose exec web python manage.py createsuperuser
docker compose ps
docker compose logs web
```

Миграции и collectstatic выполняются при старте. Gunicorn обслуживает Django, WhiteNoise — статику админки. Bootstrap загружается с CDN и требует интернет. SQLite сохраняется в томе `sqlite_data`; обычный `docker compose down` его сохраняет, `down -v` удаляет данные. Локальная база автоматически на сервер не переносится.

Для проверки сохранности создайте тему, выполните `docker compose up -d --force-recreate` и убедитесь, что тема осталась.

## Vercel

Создавайте отдельный новый проект для этого репозитория. Используется встроенная поддержка Django и Python 3.12. Нужна отдельная постоянная PostgreSQL-база: файловая SQLite не подходит для Vercel Functions.

Добавьте DATABASE_URL, DJANGO_SECRET_KEY, DJANGO_DEBUG=False, DJANGO_USE_HTTPS=True, DJANGO_ALLOWED_HOSTS и DJANGO_CSRF_TRUSTED_ORIGINS с фактическим доменом. Автоматические VERCEL_URL и VERCEL_PROJECT_PRODUCTION_URL также добавляются в разрешённые хосты. Укажите DATABASE_URL локально через защищённый .env, затем выполните `python manage.py migrate` и `python manage.py createsuperuser` перед публикацией. Не запускайте миграции или создание администратора при каждом HTTP-запросе. Vercel собирает статику автоматически.

## Проверки

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py collectstatic --noinput
```

Тесты работают с отдельной базой и проверяют вход, регистрацию, выход, админку, создание/редактирование, приватность, отсутствующие ID и безопасные перенаправления. Для production дополнительно запускайте `python manage.py check --deploy` с реальными настройками. На HTTP учебного сервера предупреждения о HTTPS ожидаемы; защищённые cookies включайте только после подключения HTTPS.

Администратор создаётся командой createsuperuser; общедоступных встроенных паролей в проекте нет.
