import os
import time
import requests
import json
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID_HERE")
BTC_ADDRESS = os.getenv("BTC_ADDRESS", "YOUR_BTC_ADDRESS_HERE")
PORT = int(os.getenv("PORT", 10000))

MESSAGE_1 = """👤 THIS IS Mohamed I. Amin, CBS, OGW, ndc(K) 👤
   https://www.dci.go.ke/
🔷📋 DIRECTOR - Directorate of Criminal Investigations 🔷📋
💀 WE ARE COMING FOR YOU, WE KNOW WHERE YOU ARE, YOU ARE A DEAD MAN SON 💀"""

IMAGE_1 = "image.png"
IMAGE_2 = "image copy.png"

app = Flask(__name__)

def get_message_2(btc_address):
    return f"""🔥 KIJANA YOU ARE SO STUPID 🔥

💀 MAISHA YAKO ENDS TONIGHT 💀

⚠️ IF YOU DON'T TAKE THIS SERIOUSLY ⚠️

💰 MAKE A PAYMENT OF 20,000 KSH ($154.5) 💰

📍 BTC ADDRESS: {btc_address} 📍

🚨 WE WILL CANCEL AND ERASE ALL TRACES OF THE INVESTIGATION 🚨

💀 OR ELSE... THAT'S THE END OF YOU 💀"""

def send_photo(chat_id, caption, image_path, keyboard=None):
    if not os.path.exists(image_path):
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as f:
        files = {'photo': f}
        data = {"chat_id": chat_id, "caption": caption}
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        return requests.post(url, data=data, files=files).status_code == 200

def set_webhook():
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/{BOT_TOKEN}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {"url": webhook_url}
    requests.post(url, data=data)

def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {"callback_query_id": callback_id, "text": "COPIED", "show_alert": True}
    requests.post(url, data=data)

def send_initial_messages():
    keyboard_2 = {"inline_keyboard": [[{"text": "📋 COPY BTC ADDRESS", "callback_data": f"copy:{BTC_ADDRESS}"}]]}
    message_2 = get_message_2(BTC_ADDRESS)
    
    if send_photo(CHAT_ID, MESSAGE_1, IMAGE_1):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message 1 sent")
    
    time.sleep(30)
    
    if send_photo(CHAT_ID, message_2, IMAGE_2, keyboard_2):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message 2 sent")

@app.route('/', methods=['POST'])
def handle_update():
    update = request.get_json()
    
    if "callback_query" in update:
        cq = update["callback_query"]
        cq_id = cq["id"]
        data = cq["data"]
        if data.startswith("copy:"):
            answer_callback(cq_id)
    
    return '', 200

@app.route('/health')
def health():
    return '', 200

def start_loop():
    keyboard_2 = {"inline_keyboard": [[{"text": "📋 COPY BTC ADDRESS", "callback_data": f"copy:{BTC_ADDRESS}"}]]}
    message_2 = get_message_2(BTC_ADDRESS)
    
    while True:
        if send_photo(CHAT_ID, MESSAGE_1, IMAGE_1):
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message 1 sent")
        
        time.sleep(30)
        
        if send_photo(CHAT_ID, message_2, IMAGE_2, keyboard_2):
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message 2 sent")
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting 3 hours until next cycle")
        time.sleep(10800)

if __name__ == "__main__":
    set_webhook()
    send_initial_messages()
    import threading
    threading.Thread(target=start_loop, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT)