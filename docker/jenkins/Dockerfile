FROM jenkins/jenkins:lts

USER root

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
