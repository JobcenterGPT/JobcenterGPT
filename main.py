import os
import telebot
from flask import Flask, request

# Загружаем токен
TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет 👋 Я бот JobcenterGPT. Чем могу помочь?")

# Обработка вебхука
@app.route(f"/{os.environ.get('BOT_TOKEN')}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Проверочная страница
@app.route('/')
def index():
    return "✅ Бот JobcenterGPT работает!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://jobcentergpt.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Принудительно сбрасываем старый webhook и ставим новый
bot.remove_webhook()
set_result = bot.set_webhook(url=f"https://jobcentergpt.onrender.com/{TOKEN}")
print("Webhook reset result:", set_result)
