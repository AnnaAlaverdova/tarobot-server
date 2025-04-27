from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Настройки: токен бота и имя канала
BOT_TOKEN = '7936809718:AAH3pwDl62XrXIrTbWwFLhFKWdxCDJGOLY8'
CHANNEL_USERNAME = '@tarocardstest'  # Имя твоего канала без пробелов

@app.route('/check_subscription', methods=['POST'])
def check_subscription():
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'ok': False, 'error': 'Не передан user_id'}), 400

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id={CHANNEL_USERNAME}&user_id={user_id}"
    response = requests.get(url)
    result = response.json()

    if result.get('ok') and result.get('result'):
        status = result['result']['status']
        if status in ['member', 'administrator', 'creator']:
            return jsonify({'subscribed': True})
        else:
            return jsonify({'subscribed': False})
    else:
        return jsonify({'ok': False, 'error': 'Ошибка Telegram API'}), 400

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
