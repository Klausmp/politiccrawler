#!/bin/bash

source .env

if [ ! -f "$VENV_PATH" ]; then
  echo "Virtual environment not found at '$VENV_PATH'. Creating one..."
  python3 -m venv venv || { echo "Failed to create virtual environment"; exit 1; }
  echo "Virtual environment created at 'venv/'."
else
  echo "Virtual environment already exists at '$VENV_PATH'."
fi

source $VENV_PATH

pip install -r requirements.txt

python src/python/update_videos.py
