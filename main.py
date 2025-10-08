import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Бот JobcenterGPT работает ✅'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот JobcenterGPT. Чем могу помочь?")

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        if data:
            update = telebot.types.Update.de_json(data)
            bot.process_new_updates([update])
        return '', 200
    except Exception as e:
        print(f"Ошибка обработки вебхука: {e}")
        return 'error', 500

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://jobcentergpt.onrender.com/{TOKEN}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
