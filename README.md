# Website Monitoring & Alert System

This project monitors websites and stores their status (UP/DOWN) and response time in a PostgreSQL database.

## How it works
- The monitor script checks each website
- It records status codes and response time
- Data is saved into the database
- The process runs automatically using cron inside Docker

## Features
- Website uptime monitoring
- Response time tracking
- Automatic database setup (no manual SQL needed)
- Runs every minute using cron
- Fully Dockerized system

## Run the project

docker-compose up --build

## Check logs (see monitoring activity)

docker exec -it website_monitor_app cat /var/log/cron.log

## Check database

docker exec -it website_monitor_db psql -U user -d monitor_db

Run:

SELECT * FROM logs;