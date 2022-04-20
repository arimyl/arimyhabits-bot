import os

from linebot import (
    LineBotApi, WebhookHandler
)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["LINE_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)