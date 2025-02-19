#!/bin/bash

docker compose down

sudo rm -r ./.postgres_data

docker compose up -d