import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "8249445313:AAFeexd7eIcE5rc8ZypgpLa_emZy_sGRfSo"
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")  # <-- вытаскиваем правильный chat_id

    if text.startswith("/translate"):
        parts = text.split(maxsplit=1)
        if len(parts) == 2:
            phrase = parts[1]
            translation = fake_translate(phrase)
            send_message(chat_id, translation)
        else:
            send_message(chat_id, "Пожалуйста, введите фразу после команды /translate")
    else:
        send_message(chat_id, "Привет! Напиши /translate [текст], и я переведу его.")

    return {"ok": True}

def send_message(chat_id, text):
    requests.post(API_URL, json={
        "chat_id": chat_id,
        "text": text
    })

def fake_translate(phrase):
    return phrase[::-1]  # просто переворачивает текст

if __name__ == "__main__":
    app.run()
