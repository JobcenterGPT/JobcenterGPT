import os
import requests
from flask import Flask, request
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

def translate_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты профессиональный переводчик. Переводи текст пользователя на нужный язык."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка при обращении к OpenAI: {e}"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        message = data["message"]
        text = message.get("text", "")
        chat_id = message["chat"]["id"]

        if text.startswith("/translate"):
            phrase = text.replace("/translate", "").strip()
            translated = translate_text(phrase)
            send_message(chat_id, translated)
        else:
            send_message(chat_id, "Напиши /translate и фразу для перевода.")
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)
