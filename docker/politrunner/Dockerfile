FROM python:3.13.2-slim

USER root

# Set working directory
WORKDIR /home/polticrawler

# Copy and install Python dependencies
COPY ./requirements.txt ./requirements.txt
# Copy prisma files
COPY ./prisma ./prisma
# Copy source files
COPY ./src/ ./src/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Generate prisma client
RUN prisma generate

# Install cron
RUN apt update && apt install -y cron && rm -rf /var/lib/apt/lists/*

# Copy crontab file into the container
COPY crontab /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron && crontab /etc/cron.d/mycron

# Ensure the log directory exists
RUN mkdir -p "./log"

# Ensure the log file exists
RUN touch ./log/cron.log

# Start cron in the background and keep the container running
CMD ["sh", "-c", "service cron start && tail -f ./log/cron.log"]
