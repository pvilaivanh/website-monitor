# Website Monitoring & Alert System

This project automatically monitors websites and stores their status in a PostgreSQL database.

## Features
- Website uptime monitoring
- Response time tracking
- Automatic database setup (no manual SQL)
- Runs every minute using cron
- Dockerized system

## Run the project

docker-compose up --build

## Check logs

docker exec -it website_monitor_app cat /var/log/cron.log

## Check database

docker exec -it website_monitor_db psql -U user -d monitor_db

SELECT * FROM logs;