import os
import telebot
from flask import Flask, request
from openai import OpenAI

# === Настройки из переменных окружения ===
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# === Статусная страница ===
@app.route("/")
def index():
    return "✅ Бот JobcenterGPT запущен и ждёт сообщений!", 200

# === Вебхук: слушаем КОРЕНЬ '/' ===
@app.route("/", methods=["POST"])
def webhook():
    # Telegram шлёт JSON
    if request.headers.get("content-type") != "application/json":
        return "Unsupported Media Type", 415

    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    print("Received update")  # будет видно в логах Render
    bot.process_new_updates([update])
    return "", 200

# === Команды ===
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Пиши: /translate <текст на английском> — переведу на немецкий 🇩🇪")

@bot.message_handler(commands=["translate"])
def translate_message(message):
    try:
        text = message.text.replace("/translate", "", 1).strip()
        if not text:
            bot.reply_to(message, "Добавь текст после /translate, например: /translate Hello world")
            return

        # OpenAI v2.x
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты переводчик. Всегда переводи на немецкий язык."},
                {"role": "user", "content": text},
            ],
        )
        translated = response.choices[0].message.content.strip()
        bot.reply_to(message, translated)
    except Exception as e:
        bot.reply_to(message, f"Ошибка перевода: {e}")

# === Запуск ===
if __name__ == "__main__":
    bot.remove_webhook()
    # ВАЖНО: вебхук на корень '/', без токена в пути
    bot.set_webhook(url="https://jobcentergpt.onrender.com/")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
