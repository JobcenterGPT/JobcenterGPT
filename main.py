import telebot
from flask import Flask, request
import openai
import os

# === Настройки ===
TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === Главная страница ===
@app.route('/')
def index():
    return '✅ JobcenterGPT работает и ждёт сообщений!'

# === Маршрут для приёма данных от Telegram ===
@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Отправь команду /translate <текст>, и я переведу с английского на немецкий 🇩🇪")

# === Команда /translate ===
@bot.message_handler(commands=['translate'])
def translate_message(message):
    try:
        text = message.text.replace('/translate', '').strip()
        print("Received:", text)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты переводчик. Переводи текст с английского на немецкий."},
                {"role": "user", "content": text}
            ]
        )

        translated = response.choices[0].message.content.strip()
        bot.reply_to(message, translated)
        print("Translated:", translated)

    except Exception as e:
        print("Ошибка:", e)
        bot.reply_to(message, f"⚠️ Ошибка перевода: {e}")

# === Обработка всех остальных сообщений ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text
        print("Received:", text)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты переводчик. Переводи текст с английского на немецкий."},
                {"role": "user", "content": text}
            ]
        )

        translated = response.choices[0].message.content.strip()
        bot.reply_to(message, translated)
        print("Translated:", translated)

    except Exception as e:
        print("Ошибка:", e)
        bot.reply_to(message, f"⚠️ Ошибка: {e}")

# === Запуск ===
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://jobcentergpt.onrender.com/{TOKEN}')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
