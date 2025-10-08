import telebot
from flask import Flask, request

TOKEN = "8249445313:AAFeexd7eIcE5rc8ZypgpLa_emZy_sGRfSo"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Бот JobcenterGPT запущен и ждёт сообщения!'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот JobcenterGPT, чем могу помочь?")

if __name__ == '__main__':
    import os
    bot.remove_webhook()
    bot.set_webhook(url=f'https://jobcentergpt.onrender.com/{TOKEN}')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
