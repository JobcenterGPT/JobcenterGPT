import os
import requests
import openai
from flask import Flask, request
from dotenv import load_dotenv  # 🆕

load_dotenv()  # 🆕

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # 🆕
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")  # <-- вытаскиваем правильный chat_id

    if text.startswith("/translate"):
        parts = text.split(maxsplit=1)
        openai.api_key = os.getenv("OPENAI_API_KEY")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты профессиональный переводчик. Переводи точно и грамотно."},
                {"role": "user", "content": f"Переведи на немецкий: {phrase}"}
            ]
        )
        translation = response.choices[0].message["content"].strip()
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
