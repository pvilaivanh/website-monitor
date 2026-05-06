# Use Python base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY app/ app/

# Create cron job (every minute)
RUN echo "* * * * * /usr/local/bin/python3 /app/app/monitor.py >> /var/log/cron.log 2>&1" > /etc/cron.d/monitor-cron

# Set permissions
RUN chmod 0644 /etc/cron.d/monitor-cron

# Apply cron job
RUN crontab /etc/cron.d/monitor-cron

# Log file
RUN touch /var/log/cron.log

# Run cron
CMD ["cron", "-f"]