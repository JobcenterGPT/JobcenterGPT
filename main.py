import requests
import json
from flask import Flask, request

app = Flask(__name__)

# 🔵 ТВОЙ TELEGRAM БОТ ТОКЕН 🔵
TOKEN = "🔵8249445313:AAFeexd7eIcE5rc8ZypgpLa_emZy_sGRfSo🔵"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# ПЕРЕВОДЧИК
def translate_text(text):
    url = "https://translate.argosopentech.com/translate"
    payload = {
        "q": text,
        "source": "en",
        "target": "ru",
        "format": "text"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json().get("translatedText")
    return "Ошибка перевода"

# ПРИЁМ СООБЩЕНИЙ
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]

        if text.startswith("/translate"):
            original_text = text.replace("/translate", "").strip()
            translated = translate_text(original_text)
            send_message(chat_id, translated)
        else:
            send_message(chat_id, "Напиши команду /translate и текст на английском.")
    
    return "ok", 200

# ОТПРАВКА СООБЩЕНИЯ
def send_message(chat_id, text):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(TELEGRAM_API_URL, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
