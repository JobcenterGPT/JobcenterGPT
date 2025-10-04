import os
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN")  # берем токен из переменных окружения Render
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Простой обработчик /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я JobcenterGPT 🤖. Бот запущен и работает!")

# Flask endpoint для Telegram Webhook
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://" + os.getenv("RENDER_EXTERNAL_HOSTNAME") + "/" + TOKEN)
    return "Webhook set", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
