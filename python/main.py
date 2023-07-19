from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/demo', methods=['GET'])
def demo_get():
    return jsonify({'msg': 'scuccess'}), 200

@app.route('/demo', methods=['POST'])
def demo_post():
    data = request.get_json()
    from_uid = data.get('from_uid')
    detail = data.get('detail')
    content = detail.get('content')

    # 发送消息
    send_message(from_uid, 'get your message')

    # 指定关键词
    if content == 'ping':
        send_message(from_uid, 'pong')

    return jsonify({'msg': 'scuccess'}), 200

def send_message(from_uid, message):
    base_url = '你的vocechat网站url'
    bot_api_key = '你的bot api key'
    endpoint = f'{base_url}/api/bot/send_to_user/{from_uid}'
    headers = {
        'Content-Type': 'text/markdown',
        'x-api-key': bot_api_key,
        'accept': 'application/json; charset=utf-8'
    }
    response = requests.post(endpoint, data=message.encode('utf-8'), headers=headers)

    # 返回消息id,当前无用
    return response.json()

if __name__ == '__main__':
    port = 4080
    app.run(host='0.0.0.0', port=port)