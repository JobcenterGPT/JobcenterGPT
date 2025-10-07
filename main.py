import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот JobcenterGPT. Чем могу помочь?")

# Webhook
@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200

# Проверочная страница
@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://jobcentergpt.onrender.com/")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
