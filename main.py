import os
import requests
import openai
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message = data.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")

    if text.startswith("/translate"):
        phrase = text.replace("/translate", "").strip()
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Шаг 1: определяем язык текста
        detection = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты определитель языка. Ответь одним словом: 'русский', 'немецкий', 'английский' и т.д."},
                {"role": "user", "content": f"На каком языке это написано: {phrase}"}
            ]
        )
        lang = detection.choices[0].message["content"].strip().lower()

        # Шаг 2: определяем, куда переводить
        if lang == "немецкий":
            target_lang = "русский"
        else:
            target_lang = "немецкий"

        # Шаг 3: делаем перевод
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Ты профессиональный переводчик. Переводи на {target_lang}."},
                {"role": "user", "content": phrase}
            ]
        )
        translation = response.choices[0].message["content"].strip()
        send_message(chat_id, f"Перевод на {target_lang}:\n{translation}")
    else:
        send_message(chat_id, "Привет! Напиши /translate [текст], и я переведу его.")

    return {"ok": True}

def send_message(chat_id, text):
    requests.post(API_URL, json={
        "chat_id": chat_id,
        "text": text
    })

if __name__ == "__main__":
    app.run()
