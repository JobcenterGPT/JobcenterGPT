import telebot
from flask import Flask, request
import openai
import os

# === Настройки ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

openai.api_key = OPENAI_API_KEY

# === Главная страница ===
@app.route('/')
def index():
    return '✅ JobcenterGPT запущен и ждёт сообщений!'

# === Webhook ===
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    try:
        json_str = request.get_data(as_text=True)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    except Exception as e:
        print(f"❌ Ошибка webhook: {e}")
    return '', 200

# === Команда /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет 👋 Я JobcenterGPT.\nНапиши /translate + текст, и я переведу его 🇩🇪")

# === Команда /translate ===
@bot.message_handler(commands=['translate'])
def translate(message):
    text = message.text.replace('/translate', '').strip()
    if not text:
        bot.reply_to(message, "❗ Введи текст после команды, например:\n/translate Hello my friend")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты профессиональный переводчик. Переводи текст с английского на немецкий."},
                {"role": "user", "content": text}
            ]
        )
        translated = response.choices[0].message["content"].strip()
        bot.reply_to(message, translated)
        print(f"✅ Перевод выполнен: {translated}")
    except Exception as e:
        print(f"⚠️ Ошибка перевода: {e}")
        bot.reply_to(message, "⚠️ Ошибка перевода. Проверь ключ OpenAI или попробуй позже.")

# === Обработка других сообщений ===
@bot.message_handler(func=lambda msg: True)
def echo(message):
    bot.reply_to(message, "💬 Используй команду /translate для перевода!")

# === Запуск ===
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://jobcentergpt.onrender.com/{BOT_TOKEN}')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
