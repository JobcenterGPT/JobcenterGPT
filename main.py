import telebot
from flask import Flask, request
import openai
import os

# === Настройки ===
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === Главная страница ===
@app.route('/')
def index():
    return '✅ JobcenterGPT активен и ждёт сообщений!'

# === Webhook для Telegram ===
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    try:
        json_str = request.get_data(as_text=True)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    except Exception as e:
        print("❌ Ошибка Webhook:", e)
    return '', 200

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет 👋 Я JobcenterGPT. Напиши /translate <текст>, и я переведу его на немецкий 🇩🇪")

# === Команда /translate ===
@bot.message_handler(commands=['translate'])
def translate_message(message):
    text = message.text.replace('/translate', '').strip()
    if not text:
        bot.reply_to(message, "❗ Введи текст после команды, например:\n/translate Hello my friend")
        return

    try:
        openai.api_key = OPENAI_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            timeout=10,
            messages=[
                {"role": "system", "content": "Ты переводчик. Переводи текст с английского на немецкий."},
                {"role": "user", "content": text}
            ]
        )
        translated = response.choices[0].message.content.strip()
        bot.reply_to(message, translated)
        print(f"✅ Перевод выполнен: {translated}")

    except Exception as e:
        print(f"⚠️ Ошибка перевода: {e}")
        bot.reply_to(message, "⚠️ Ошибка перевода. Проверь ключ OpenAI или попробуй позже.")

# === Обработка всех остальных сообщений ===
@bot.message_handler(func=lambda msg: True)
def echo_message(message):
    bot.reply_to(message, "💬 Используй /translate для перевода!")

# === Запуск ===
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://jobcentergpt.onrender.com/{TOKEN}')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
