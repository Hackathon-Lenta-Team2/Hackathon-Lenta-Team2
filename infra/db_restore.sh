#!/bin/bash

echo  "Starting DB restoration using dump_db_hakathon.sql"
# в директории infra/
# копировать дамп в контейнер c БД
docker compose cp ./dump_db_hakathon.sql db:var/lib/postgresql/
# удалить и заново создать БД
docker compose exec db dropdb postgres
docker compose exec db createdb postgres
# восстановить данные
docker compose exec db pg_restore -d postgres var/lib/postgresql/dump_db_hakathon.sql

echo  "DB restoration finished successfully."

sleep 2