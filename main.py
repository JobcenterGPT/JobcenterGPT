import telebot
from flask import Flask, request
import openai
import os

# === Настройки ===
TOKEN = os.getenv("BOT_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === Основная страница ===
@app.route('/')
def index():
    return '✅ Бот JobcenterGPT запущен и ждёт сообщений!'

# === Webhook ===
@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        json_str = request.get_data(as_text=True)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Bot is running!', 200
@bot.message_handler(commands=['translate'])
def translate_message(message):
    try:
    text = message.text
    print("Received:", text)  # эта строка должна быть с тем же отступом, что и text = message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты переводчик. Переводи текст на немецкий язык."},
            {"role": "user", "content": text}
        ]
    )

    translated = response.choices[0].message.content.strip()
    bot.reply_to(message, translated)

except Exception as e:
    bot.reply_to(message, f"Ошибка перевода: {e}")
# === Обработка сообщений ===
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text
        response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Ты переводчик. Переводи текст на немецкий язык."},
        {"role": "user", "content": text}
    ]
)

print("Received:", text)  # 👉 эта строка просто покажет входящее сообщение в логах Render
translated = response.choices[0].message.content.strip()  # 👉 здесь точка, не скобки
bot.reply_to(message, translated)
    except Exception as e:
        bot.reply_to(message, f"Ошибка перевода: {e}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f'https://jobcentergpt.onrender.com/{TOKEN}')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
