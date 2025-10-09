import os
from flask import Flask, request
import requests

app = Flask(__name__)

# === НАСТРОЙКИ ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or "ТВОЙ_ТОКЕН_ОТСЮДА_fatherbot"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "ТВОЙ_API_КЛЮЧ_OPENAI"  # если используешь OpenAI

# === ОБРАБОТЧИК ГЛАВНОГО ВЕБХУКА ===
@app.route("/", methods=["POST"])
def webhook():
    update = request.get_json()
    print("Received update:", update)  # лог для Render

    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"]

        # === ПРОСТОЙ ПЕРЕВОД АНГЛИЙСКИЙ -> РУССКИЙ ===
        if text.startswith("/translate"):
            original_text = text.replace("/translate", "").strip()
            translated_text = translate_text(original_text)
            send_message(chat_id, translated_text)
        else:
            send_message(chat_id, "Отправь команду /translate <текст> для перевода.")
    return "ok", 200  # обязательно

# === ФУНКЦИЯ ОТПРАВКИ СООБЩЕНИЯ В ТЕЛЕГРАМ ===
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# === ФУНКЦИЯ ПЕРЕВОДА ===
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

# === ПРОСТОЙ ГЕТ МАРШРУТ ДЛЯ ПРОВЕРКИ ===
@app.route("/", methods=["GET"])
def index():
    return "JobcenterGPT is active ✅", 200

# === ЗАПУСК ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
