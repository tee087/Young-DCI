import os
import time
import requests
import json

BOT_TOKEN = "8788152580:AAGKnqqc91PxIUe7Nu2CeYAmHgBt7gWJpdM"
CHAT_ID = "7867527304"
BTC_ADDRESS = "19QjFZbTzEd8VPvkVdr2KzTVzC3Zq2qR9M"

MESSAGE_1 = """👤 THIS IS Mohamed I. Amin, CBS, OGW, ndc(K) 👤
   https://www.dci.go.ke/
🔷📋 DIRECTOR - Directorate of Criminal Investigations 🔷📋
💀 WE ARE COMING FOR YOU, WE KNOW WHERE YOU ARE, YOU ARE A DEAD MAN SON 💀"""

MESSAGE_2 = """🔥 KIJANA YOU ARE SO STUPID 🔥

💀 MAISHA YAKO ENDS TONIGHT 💀

⚠️ IF YOU DON'T TAKE THIS SERIOUSLY ⚠️

💰 MAKE A PAYMENT OF 20,000 KSH ($154.5) 💰

📍 BTC ADDRESS: 19QjFZbTzEd8VPvkVdr2KzTVzC3Zq2qR9M 📍

🚨 WE WILL CANCEL AND ERASE ALL TRACES OF THE INVESTIGATION 🚨

💀 OR ELSE... THAT'S THE END OF YOU 💀"""

IMAGE_1 = "image.png"
IMAGE_2 = "image copy.png"

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

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    data = {"offset": offset}
    return requests.post(url, data=data).json()

def answer_callback(callback_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/answerCallbackQuery"
    data = {"callback_query_id": callback_id, "text": "COPIED", "show_alert": True}
    requests.post(url, data=data)

def process_callbacks(last_update_id):
    try:
        resp = get_updates(offset=last_update_id)
        new_last = last_update_id
        for update in resp.get("result", []):
            if "callback_query" in update:
                cq = update["callback_query"]
                cq_id = cq["id"]
                data = cq["data"]
                if data.startswith("copy:"):
                    answer_callback(cq_id)
            if "update_id" in update:
                new_last = update["update_id"] + 1
        return new_last
    except:
        return last_update_id

def main():
    print(f"Bot started. Sending messages: Msg1 -> 30 sec -> Msg2 -> 3 hours -> repeat")
    
    last_update_id = 0
    try:
        resp = get_updates()
        if resp.get("ok") and resp.get("result"):
            last_update_id = resp["result"][-1].get("update_id", 0) + 1
    except:
        pass
    
    keyboard_2 = {"inline_keyboard": [[{"text": "📋 COPY BTC ADDRESS", "callback_data": f"copy:{BTC_ADDRESS}"}]]}
    
    while True:
        if send_photo(CHAT_ID, MESSAGE_1, IMAGE_1):
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message 1 sent")
        
        last_update_id = process_callbacks(last_update_id)
        
        time.sleep(30)
        
        if send_photo(CHAT_ID, MESSAGE_2, IMAGE_2, keyboard_2):
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message 2 sent")
        
        last_update_id = process_callbacks(last_update_id)
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting 3 hours until next cycle")
        time.sleep(10800)

if __name__ == "__main__":
    main()