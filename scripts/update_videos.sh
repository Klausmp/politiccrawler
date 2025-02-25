#!/bin/bash

source .env

if [ ! -d "venv" ]; then
  echo "Virtual environment not found. Creating one..."
  python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }
  echo "Virtual environment created at 'venv/'."
else
  echo "Virtual environment already exists."
fi

source venv/bin/activate

pip install -r requirements.txt

python src/python/update_videos.py
