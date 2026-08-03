# Telegram DCI Scary Message Bot

A simple Telegram bot that sends a scary message every 1 minute.

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export BOT_TOKEN="your_bot_token"
export CHAT_ID="your_chat_id"
```

Or copy `.env.example` to `.env` and fill in values.

3. Get your bot token from @BotFather on Telegram.

4. To get your CHAT_ID:
   - Start a chat with @userinfobot
   - Or use @myidbot

## Running

```bash
python bot.py
```

The bot will send the DCI scary message with an image (if `scary_image.jpg` exists) every 60 seconds.