import re

from linebot import LineBotApi
from linebot.models import TextSendMessage

from modules.compose_message import compose_template_message, MessageType
from modules.operate_message import register_message
from modules.operate_firebase import (
    get_message_types,
    get_user_info_from_user_id,
    register_tmp,
)

# conf
include_digit = re.compile("\s")


def line_conversation(event, line_bot_api: LineBotApi):
    """reply line message. register or get tmp-data at DB.
    :event: line webhook request data
    :line_bot_api: line account api for replying message
    """
    message_text = event.message.text
    user_id = event.source.user_id
    user_info = get_user_info_from_user_id(user_id)
    doc_id = user_info.id

    register_message(message_text, doc_id)

    # register_tmporary(message_text, doc_id)

    # compose message
    message_objs = []
    # if greeting(message_text): # 挨拶
    greeting = check_greeting(message_text)  # 挨拶
    if greeting:
        message_objs.append(TextSendMessage(text=greeting))

    if message_text.isdigit():  # 数値
        message_objs.append(
            compose_template_message(
                MessageType.button, "What number is this?", get_message_types(doc_id)
            )
        )

    # reply
    if not (message_objs):
        message_objs = [TextSendMessage(text=message_text)]

    line_bot_api.reply_message(event.reply_token, message_objs)


def check_greeting(message: str) -> str:
    """挨拶判定を行い、同じ挨拶を返す"""
    greetings = ["hello", "おはよう", "こんにちは", "こんばんは"]
    greeting_list = list(map(lambda x: x if x in message.lower() else "", greetings))
    return "".join(greeting_list)


if __name__ == "__main__":
    pass
