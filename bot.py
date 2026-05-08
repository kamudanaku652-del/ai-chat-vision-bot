#!/usr/bin/env python3
"""
Telegram Bot - Chat & Image Vision
Gratis, tanpa API key bayar
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ai_engine import chat_with_ai, analyze_image

# Load environment
load_dotenv()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di .env")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command handler"""
    welcome_text = """
👋 Welcome to AI Chat Vision Bot!

🤖 Aku bisa:
✅ Chat dengan kamu
✅ Analisis gambar
✅ Jawab pertanyaan

📝 Cara Pakai:
1. Ketik pertanyaan apa saja
2. Atau kirim gambar + pertanyaan
3. Tunggu jawaban AI

💡 Contoh:
- "Apa itu Python?"
- Kirim gambar: "Apa yang ada di gambar ini?"

Let's chat! 🚀
    """
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command"""
    help_text = """
🆘 Help Commands:

/start - Mulai bot
/help - Bantuan ini
/about - Tentang bot

💬 Chat:
- Ketik pertanyaan apa saja

🖼️ Gambar:
- Kirim gambar (JPG, PNG)
- Tambahkan caption/pertanyaan
- Bot akan analisis

⚠️ Rate Limit:
- Free tier Hugging Face ada limit
- Tunggu beberapa detik antar request

Need help? Tanya aja! 😊
    """
    await update.message.reply_text(help_text)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """About command"""
    about_text = """
📱 AI Chat Vision Bot

🔧 Tech:
- Python + python-telegram-bot
- Hugging Face AI Models
- Open Source

💰 Cost: FREE!
- Tidak ada biaya tersembunyi
- Tidak perlu API key bayar
- Community powered

🌐 Links:
- GitHub: github.com/kamudanaku652-del/ai-chat-vision-bot

👨‍💻 Made with ❤️
    """
    await update.message.reply_text(about_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages"""
    try:
        user_message = update.message.text
        user_id = update.effective_user.id
        
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        logger.info(f"User {user_id}: {user_message}")
        
        # Get AI response
        response = chat_with_ai(user_message)
        
        # Send response (split jika terlalu panjang)
        if len(response) > 4096:
            for i in range(0, len(response), 4096):
                await update.message.reply_text(response[i:i+4096])
        else:
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}\n\nCoba lagi nanti ya!")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle image messages"""
    try:
        # Show typing indicator
        await update.message.chat.send_action("typing")
        
        # Get image
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # Download image
        image_path = f"temp_image_{update.effective_user.id}.jpg"
        await file.download_to_drive(image_path)
        
        # Get caption/question
        question = update.message.caption or "Apa yang ada di gambar ini?"
        
        logger.info(f"User {update.effective_user.id} sent image: {question}")
        
        # Analyze image
        response = analyze_image(image_path, question)
        
        # Send response
        if len(response) > 4096:
            for i in range(0, len(response), 4096):
                await update.message.reply_text(response[i:i+4096])
        else:
            await update.message.reply_text(response)
        
        # Clean up
        if os.path.exists(image_path):
            os.remove(image_path)
            
    except Exception as e:
        logger.error(f"Error handling image: {e}")
        await update.message.reply_text(f"❌ Error menganalisis gambar: {str(e)}")


def main():
    """Start the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    
    # Start bot
    logger.info("🤖 Bot started! Polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
