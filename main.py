import telebot
from flask import Flask, request
from openai import OpenAI
import os

# === Настройки ===
TOKEN = "8249445313:AAFeexd7eIcE5rc8ZypgpLa_emZy_sGRfSo"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "вставь_сюда_свой_openai_api_ключ"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)

# === Основная страница ===
@app.route('/')
def index():
    return '✅ Бот JobcenterGPT запущен и ждёт сообщения!'

# === Webhook ===
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# === Обработка сообщений ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты переводчик. Переводи все сообщения пользователя на немецкий язык."},
                {"role": "user", "content": text}
            ]
        )
        translated = completion.choices[0].message.content
        bot.reply_to(message, translated)
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://jobcentergpt.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
