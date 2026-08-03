import os
import time
import requests
import json
from flask import Flask, request
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BTC_ADDRESS = os.getenv("BTC_ADDRESS", "YOUR_BTC_ADDRESS_HERE")
PORT = int(os.getenv("PORT", 10000))

if not BOT_TOKEN or not CHAT_ID:
    logger.error("BOT_TOKEN and CHAT_ID environment variables required")
    exit(1)

MESSAGE_1 = """👤 THIS IS Mohamed I. Amin, CBS, OGW, ndc(K) 👤
   https://www.dci.go.ke/
🔷📋 DIRECTOR - Directorate of Criminal InvestigATIONS 🔷📋
💀 WE ARE COMING FOR YOU, WE KNOW WHERE YOU ARE, YOU ARE A DEAD MAN SON 💀"""

IMAGE_1 = "image.png"
IMAGE_2 = "image copy.png"

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
        logger.error(f"Image not found: {image_path}")
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as f:
        files = {'photo': f}
        data = {"chat_id": chat_id, "caption": caption}
        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)
        resp = requests.post(url, data=data, files=files)
        if resp.status_code == 200:
            logger.info(f"Message sent to {chat_id}")
            return True
        else:
            logger.error(f"Failed: {resp.text}")
            return False

def answer_callback(callback_id, text="COPIED"):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {"callback_query_id": callback_id, "text": text, "show_alert": True}
    resp = requests.post(url, data=data)
    logger.info(f"Callback answered: {resp.status_code}")

def send_message_cycle():
    keyboard_2 = {"inline_keyboard": [[{"text": "📋 COPY BTC ADDRESS", "callback_data": f"copy:{BTC_ADDRESS}"}]]}
    message_2 = get_message_2(BTC_ADDRESS)
    
    logger.info("Starting message cycle...")
    
    if send_photo(CHAT_ID, MESSAGE_1, IMAGE_1):
        logger.info("Message 1 sent successfully")
    time.sleep(30)
    
    if send_photo(CHAT_ID, message_2, IMAGE_2, keyboard_2):
        logger.info("Message 2 sent successfully")
    
    return True

def start_background_messenger():
    try:
        send_message_cycle()
    except Exception as e:
        logger.error(f"Error in background messenger: {e}")

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_update():
    try:
        update = request.get_json()
        if update and "callback_query" in update:
            cq = update["callback_query"]
            cq_id = cq["id"]
            chat_id = cq["from"]["id"]
            data = cq.get("data", "")
            if data.startswith("copy:"):
                address = data[5:]
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(url, data={"chat_id": chat_id, "text": address})
                answer_callback(cq_id, "Sent!")
    except Exception as e:
        logger.error(f"Error handling update: {e}")
    return '', 200

@app.route('/health', methods=['GET'])
def health():
    return 'OK', 200

threading.Thread(target=start_background_messenger, daemon=True).start()

if __name__ == "__main__":
    logger.info("Bot starting...")
    send_message_cycle()
    logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=PORT)