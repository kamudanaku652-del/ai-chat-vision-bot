#!/bin/bash

# Run both bot and web app
echo "🚀 Starting AI Chat Vision Bot..."

# Load environment
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Run bot in background
echo "📱 Starting Telegram Bot..."
python bot.py &
BOT_PID=$!

# Run web app
echo "🌐 Starting Web App..."
python app.py

# Cleanup
kill $BOT_PID 2>/dev/null
