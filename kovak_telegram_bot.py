import telebot
import threading
import time
from automation import run_browser

BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Kovak, send me the link to the offer you want me to complete."
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if not url.startswith("http"):
        bot.reply_to(
            message,
            "That is not a valid link. Send a link starting with http."
        )
        return

    bot.reply_to(message, "Received link. Starting browser...")

    thread = threading.Thread(
        target=run_browser,
        args=(url, message.chat.id, bot)
    )
    thread.start()


print("Bot is running...")
bot.infinity_polling()
