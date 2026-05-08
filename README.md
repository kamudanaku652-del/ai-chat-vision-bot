# AI Chat Vision Bot 🤖

Telegram Bot + Web App untuk chat dan analisis gambar dengan AI (gratis!)

## Features
✅ Chat dengan AI
✅ Analisis gambar
✅ Telegram Bot integration
✅ Web App simple
✅ 100% Gratis

## Setup

### 1. Clone Repository
```bash
git clone https://github.com/kamudanaku652-del/ai-chat-vision-bot.git
cd ai-chat-vision-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
Buat file `.env`:
```
TELEGRAM_BOT_TOKEN=8672140644:AAGy1THmd0yNFCQYLqi9d4VgFieOhS9Yxvg
HUGGING_FACE_API_URL=https://api-inference.huggingface.co/models
```

### 4. Run Bot
```bash
python bot.py
```

### 5. Run Web App (terpisah)
```bash
python app.py
```
Buka: http://localhost:5000

## Deploy ke Replit (Gratis)

1. Buka https://replit.com
2. Click "New Replit"
3. Import dari GitHub: `kamudanaku652-del/ai-chat-vision-bot`
4. Setup Secret (Environment Variables):
   - `TELEGRAM_BOT_TOKEN`: Token bot kamu
5. Click Run

## Cara Pakai

### Telegram Bot
1. Cari bot di Telegram dengan username bot kamu
2. Ketik `/start`
3. Chat atau kirim gambar

### Web App
1. Buka http://localhost:5000 (local) atau URL Replit
2. Ketik pertanyaan
3. Kirim gambar

## Tech Stack
- Python + Flask
- python-telegram-bot
- Hugging Face API (gratis)
- Streamlit (optional)

## API yang Dipakai
- Hugging Face Inference API (gratis)
- Text Generation
- Image Recognition

## License
MIT
