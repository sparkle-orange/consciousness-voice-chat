#!/bin/bash
# Run Orange Voice Listener

cd "$(dirname "$0")"

# Load environment
set -a
source .env
set +a

# Activate venv and run
source venv/bin/activate
python3 orange_voice_listener.py
