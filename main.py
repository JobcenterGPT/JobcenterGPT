import os
from flask import Flask, request
import requests
from dotenv import load_dotenv

# Загружаем .env, если запускаешь локально
load_dotenv()

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # пока не используем, пусть будет

# Flask app
app = Flask(__name__)

# === Обработка Telegram webhook ===
@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    print("Received update:", update)

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        if text.startswith("/translate "):
            original_text = text.replace("/translate", "").strip()
            translated_text = translate_text(original_text)
            send_message(chat_id, translated_text)
        else:
            send_message(chat_id, "Пришли команду /translate <текст для перевода>")
    return "OK", 200

# === Отправка сообщения в Telegram ===
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    print("TELEGRAM RESPONSE:", response.status_code, response.text)

# === Перевод текста через MyMemory API ===
def translate_text(text):
    try:
        url = "https://api.mymemory.translated.net/get"
        params = {"q": text, "langpair": "en|ru"}
        response = requests.get(url, params=params)
        data = response.json()
        return data["responseData"]["translatedText"]
    except Exception as e:
        print("Translation error:", e)
        return "Ошибка перевода."

# === Проверка сервиса ===
@app.route("/", methods=["GET"])
def index():
    return "JobcenterGPT is active ✅", 200

# === Запуск ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
