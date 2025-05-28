from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message')
    user_name = data.get('user', 'Гость')

    if not user_message:
        return jsonify({"error": "No message"}), 400

    text = f"<b>Сообщение с сайта от {user_name}:</b>\n{user_message}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }

    response = requests.post(url, json=payload)

    if response.ok:
        return jsonify({"reply": "Спасибо! Мы получили ваше сообщение."})
    else:
        return jsonify({"error": "Ошибка при отправке в Telegram"}), 500

@app.route('/')
def home():
    return "Сервер работает!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)