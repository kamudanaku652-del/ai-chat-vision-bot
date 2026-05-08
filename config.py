#!/usr/bin/env python3
"""
Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot Config
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BOT_POLLING_TIMEOUT = int(os.getenv('BOT_POLLING_TIMEOUT', 30))

# Flask Config
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))

# AI Config
HF_API_TOKEN = os.getenv('HUGGING_FACE_API_TOKEN')
MODEL_TEXT = os.getenv('MODEL_TEXT', 'gpt2')
MODEL_IMAGE = os.getenv('MODEL_IMAGE', 'Salesforce/blip-image-captioning-base')

# Limits
MAX_MESSAGE_LENGTH = 1000
MAX_IMAGE_SIZE = 16 * 1024 * 1024  # 16MB

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
