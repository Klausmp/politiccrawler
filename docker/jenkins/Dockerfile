
FROM jenkins/jenkins:lts

USER root

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

USER jenkins
