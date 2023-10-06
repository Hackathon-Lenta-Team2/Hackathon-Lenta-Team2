# Hackathon-Lenta-Team2
Совместный проект выпускников ЯП для сети гипермаркетов "Лента".
    
Целью данного проекта было создание сервиса, способного прогнозировать спрос на товары собственного производства, что позволило бы сети гипермаркетов оптимизировать свои запасы и улучшить предложение товаров для потребителей.
    
Для достижения этой цели команда проекта провела глубокий анализ данных, используя различные методы машинного обучения, а также разработала алгоритмы и модели, которые позволили бы с высокой точностью предсказывать спрос на товары.
      
## Как запустить проект локально

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/Hackathon-Lenta-Team2/Hackathon-Lenta-Team2.git
cd Hackathon-Lenta-Team2/infra/
```
Перейти в ветку dev
```bash
git checkout dev
```
В директории infra/ создать файл .env и заполнить его согласно шаблону, 
который вы можете найти в файле `.env.example`
```bash
cat .\.env.example > .env
```
Развернуть проект:
``` bash
# в директории infra/
# убедитесь, что Docker установлен и запущен на вашем ПК
docker-compose up -d
```

Проект станет доступен по адресу: [Hackathon-Lenta-Team2](http://127.0.0.1/)

Чтобы остановить проект, выполните команду:
```bash
# в директории infra/
docker-compose down
```

Документация к проекту: [Документация](http://127.0.0.1/docs/)

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
Данные для входа в админ зону:
```bash
username: admin
password: admin
```
