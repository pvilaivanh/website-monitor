FROM python:3.10

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/

# Add cron job
RUN echo "* * * * * /usr/local/bin/python3 /app/app/monitor.py >> /var/log/cron.log 2>&1" > /etc/cron.d/monitor-cron

# Give permissions
RUN chmod 0644 /etc/cron.d/monitor-cron

# Apply cron job
RUN crontab /etc/cron.d/monitor-cron

# Create log file
RUN touch /var/log/cron.d

CMD ["cron", "-f"]