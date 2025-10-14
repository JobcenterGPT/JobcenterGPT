import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "8249445313:AAFeexd7eIcE5rc8ZypgpLa_emZy_sGRfSo"
CHAT_ID = "5556229951"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")

    if text.startswith("/translate"):
        parts = text.split(maxsplit=1)
        if len(parts) == 2:
            phrase = parts[1]
            # Простой "перевод": просто меняет язык местами
            translation = fake_translate(phrase)
            send_message(translation)
        else:
            send_message("Пожалуйста, введите фразу после команды /translate.")
    else:
        send_message("Привет! Напиши /translate [текст], и я переведу его.")

    return {"ok": True}

def send_message(text):
    requests.post(API_URL, json={
        "chat_id": CHAT_ID,
        "text": text
    })

def fake_translate(phrase):
    # Заглушка — можно подключить ChatGPT, DeepL или Google API
    return f"Перевод: {phrase[::-1]}"  # просто переворачивает текст

if __name__ == "__main__":
    app.run()
