import os
import json
from flask import Flask, request
from urllib.request import Request, urlopen

# Токен берём из переменной окружения BOT_TOKEN (как сейчас у тебя на Render).
TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Бот JobcenterGPT работает ✅", 200

def tg_send(chat_id: int, text: str):
    """Прямой вызов Telegram API без сторонних библиотек."""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"})
    urlopen(req)  # если будет ошибка — увидим её в логах Render

@app.route(f"/{os.environ.get('BOT_TOKEN')}", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    # чтобы видеть, что реально прилетает от Telegram:
    print("UPDATE:", json.dumps(update, ensure_ascii=False))

    msg = (
        update.get("message")
        or update.get("edited_message")
        or (update.get("callback_query") or {}).get("message")
    )
    if not msg:
        return "ok", 200

    chat_id = msg["chat"]["id"]
    text = (msg.get("text") or "").strip()

    if text.startswith("/start"):
    tg_send(chat_id, "Привет! Я бот JobcenterGPT. Я на связи 🚀")

elif text.startswith("/translate"):
    phrase = text.replace("/translate", "").strip()
    if not phrase:
        tg_send(chat_id, "Отправь фразу после команды /translate, например:\n/translate Hallo, wie geht es dir?")
    else:
        import requests
        import json

        # Твой OpenAI API ключ
        OPENAI_API_KEY = "sk-ВСТАВЬ_СВОЙ_КЛЮЧ_ОТСЮДА_https://platform.openai.com/api-keys"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        data = {
            "model": "gpt-4o-mini",
            "input": f"Переведи это естественно на противоположный язык (русский или немецкий): {phrase}"
        }

        response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            translated = result["output"][0]["content"][0]["text"]
            tg_send(chat_id, f"Перевод:\n{translated}")
        else:
            tg_send(chat_id, f"Ошибка перевода ({response.status_code}): {response.text}")

else:
    tg_send(chat_id, f"Эхо: {text}")

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
