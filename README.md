# Telegram DCI Scary Message Bot

A Telegram bot that sends scary messages every 3 hours.

## Environment Variables

Set these on Render or your deployment platform:

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Your Telegram bot token from @BotFather |
| `CHAT_ID` | Target chat ID to receive messages |
| `BTC_ADDRESS` | Bitcoin address for payment button |

## Deployment on Render

1. Connect your GitHub repo
2. Create a **Background Worker**
3. Set environment variables in Render dashboard:
   - `BOT_TOKEN=your_bot_token`
   - `CHAT_ID=your_chat_id`
   - `BTC_ADDRESS=your_btc_address`
4. Set **Start Command**: `python bot.py`

## Local Testing

```bash
BOT_TOKEN=your_token CHAT_ID=your_id python bot.py
```

## Message Schedule

1. Message 1 sent (with image.png)
2. 30 seconds later → Message 2 sent (with image copy.png + COPY button)
3. 3 hours → Repeat from step 1

## Images Required

- `image.png` - First message image
- `image copy.png` - Second message image (with inline COPY BTC ADDRESS button)