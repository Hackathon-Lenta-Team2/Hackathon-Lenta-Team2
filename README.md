# Hackathon-Lenta-Team2
Совместный проект 10 выпускников ЯП в рамках Хакатона для сети гипермаркетов "Лента".
    
Целью данного проекта было создание сервиса, способного прогнозировать спрос на товары собственного производства, что позволило бы сети гипермаркетов оптимизировать свои запасы и улучшить предложение товаров для потребителей.
    
Для достижения этой цели команда проекта провела глубокий анализ данных, используя различные методы машинного обучения, а также разработала алгоритмы и модели, которые позволили бы предсказывать спрос на товары.

В данном репозитории находится общая сборка работ всех команд.

### Ссылки на репозитории отдельных направлений:
- [🔗Frontend](https://github.com/Hackathon-Lenta-Team2/frontend)
- [🔗Design](https://www.figma.com/file/2Mxz9r4EpsNjL8mJFgRQgM/%D0%9B%D0%B5%D0%BD%D1%82%D0%B0.-%D0%94%D0%B8%D0%B7%D0%B0%D0%B9%D0%BD?type=design&node-id=52%3A432&mode=design&t=t3UMucqylrbL4jSm-1)
- [🔗Data Science](https://github.com/Hackathon-Lenta-Team2/ds)

## Как запустить проект:
#### Загрузить модель машинного обучения по ссылке: [🔗DS Model](https://drive.google.com/file/d/1_hg6Ik4bL5PoKDJzi39wJ1R5K67L0H8K/view)
<details>
<summary>Команды для запуска вручную</summary>

Клонировать репозиторий и перейти в папку `infra` в командной строке.
```bash
git clone https://github.com/Hackathon-Lenta-Team2/Hackathon-Lenta-Team2.git
cd Hackathon-Lenta-Team2/infra/
```

В директории infra/ создать файл `.env` и `.env.ds`, заполнить их согласно шаблонам, 
которые вы можете найти в файлах `.env.example` и `.env.example_ds`.
```bash
cat ./.env.example > .env
cat ./.env.example_ds > .env.ds
```
Положить файл с моделью `rf.joblib` в папку `ds/scripts/src/`.

Развернуть проект:
``` bash
# в директории infra/
# убедитесь, что Docker установлен и запущен на вашем ПК
docker-compose up -d
```

Для заполнения БД готовыми данными можно воспользоваться командами:
``` bash
# в директории infra/
# копировать дамп в контейнер c БД
docker compose cp ./dump_db_hakathon.sql db:var/lib/postgresql/

# удалить и заново создать БД
docker compose exec db dropdb postgres
docker compose exec db createdb postgres

# восстановить данные
docker compose exec db pg_restore -d postgres var/lib/postgresql/dump_db_hakathon.sql
```
Данные для входа в [🔗Админ-зону](http://127.0.0.1/admin/):
```bash
username: admin
password: admin
```
</details>

<details>
<summary>Инструкция с автоматическим запуском контейнеров</summary>

#### 1. Клонировать репозиторий и перейти в него в командной строке.
```bash
git clone https://github.com/Hackathon-Lenta-Team2/Hackathon-Lenta-Team2.git
# перейти в папку для дальнейшего шага
cd Hackathon-Lenta-Team2/ds/scripts/src/
```
#### 2. Положить файл с моделью `rf.joblib` в папку `ds/scripts/src/`.

#### 3. Развернуть проект:
<details>
<summary>для пользователей Windows:</summary>

#### Убедитесь что Git Bash установлен на вашем ПК
``` bash
# в директории infra\
# убедитесь, что Docker установлен и запущен на вашем ПК
.\run.sh
# дождитесь уведомления "Service started successfully."
# в терминале
```
#### Для восстановления БД:
``` bash
.\db_restore.sh
```
</details>
<details>
<summary>для пользователей Unix/Linux:</summary>

``` bash
# в директории infra/
# убедитесь, что Docker установлен и запущен на вашем ПК
sh run.sh
# дождитесь уведомления "Service started successfully."
# в терминале
```
#### Для восстановления БД:
``` bash
sh db_restore.sh
```
</details>

#### 4. Данные для входа в [🔗Админ-зону](http://127.0.0.1/admin/):
```bash
username: admin
password: admin
```
</details>

### После запуска

Проект станет доступен по адресу: [🔗Hackathon-Lenta-Team2](http://127.0.0.1/)

Чтобы остановить проект, выполните команду:
```bash
# в директории infra/
docker-compose down
```
Если вам не нужны готовые данные, выполните команду создания
суперпользователя для входа в админ-зону:
``` bash
# в директории infra/
# создать суперпользователя
docker-compose exec back python manage.py createsuperuser
```
### Документация API

<details>
<summary>Документация к API скриншот 📸</summary>

 ![Документация к API](readme_data/API_docs_screenshot.png)
</details>

#### В запущенном сервисе:

Документация к API доступна [🔗Здесь](http://127.0.0.1/docs/)

Авто-документация (drf-spectacular) [🔗Здесь](http://127.0.0.1/docs-auto/)

## Архитектура бэкенда
<details>
<summary>Стек технологий</summary>

- Postgres
- Django, Django REST Framework, Djoser, Drf-spectacular
- Django UnitTest, Factory-boy
- Celery, Flower, Gunicorn, Loguru, Pandas, Redis
- Requests, XlsxWriter

</details>

<details>
<summary>Схема БД на этапе планирования</summary>

![Схема докер контейнеров](readme_data/db_overview.png)
</details>

<details>
<summary>Схема работы Docker Compose</summary>

![Схема докер контейнеров](readme_data/containers_schema.png)
</details>

<details>
<summary>Data Flow</summary>


![Coverage](readme_data/data_flow.png)
</details>

<details>
<summary>Тестирование проекта</summary>

В рамках Хакатона добились покрытия в 85%

![Coverage](readme_data/coverage.png)
</details>