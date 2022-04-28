import re
from typing import List

from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    ConfirmTemplate, ButtonsTemplate
)

from settings.line_init import line_bot_api


# conf
include_digit = re.compile('\s')

def line_conversation(event):
    message_text = event.message.text
    user_id = event.source.user_id
    
    # compose message
    message_objs = []
    # if greeting(message_text): # 挨拶
    greeting = check_greeting(message_text) # 挨拶
    if greeting:
        message_objs.append(TextSendMessage(text=greeting))

    if message_text.isdigit(): # 数値
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=message_text),
                compose_message('confirm', 'What number is this?')
            ]
        )
    
    # reply
    if not(message_objs):
        message_objs = [TextSendMessage(text=message_text)]

    line_bot_api.reply_message(
        event.reply_token,
        message_objs
    )

    
def check_greeting(message:str) -> str:
    """挨拶判定を行い、同じ挨拶を返す"""
    greetings = ['hello', 'おはよう', 'こんにちは', 'こんばんは']
    # greetings check
    # if sum(list(map(lambda x: x in message.lower(), greetings))):
        # return message
    # return ''
    greeting_list = list(map(lambda x: x if x in message.lower() else '', greetings))
    return ''.join(greeting_list)


def compose_message(type: str, text: str, items: List[dict]=None) -> TemplateSendMessage:
    """TemplateMessageの選択"""
    if type == 'confirm':
        tmp = ConfirmTemplate(
            text, confirm_actions
        )
    elif type == 'button':
        tmp = ButtonsTemplate(
            text, compose_type_button(items)
        )
    else:
        tmp

    return TemplateSendMessage('this is a template', tmp)


def compose_type_button(types: List[dict]) -> List[dict]:
    """typesからbutton actionを作成
    :types: type of text message. 
    :return [button_action, ...]
    """
    if types is None:
        types = []

    buttons_actions = []
    for i in types:
        action = {
            'type': 'message',
            'label': i.name,
            'text': i.num
        }
        buttons_actions.append(action)
    buttons_actions.append({
        'type': 'message',
        'label': '新規追加',
        'text': '0'
    })

    return buttons_actions


confirm_actions = [
    {
        "type": "message",
        "label": "はい",
        "text": "はい"
    },
    {
        "type": "message",
        "label": "いいえ",
        "text": "いいえ"
    }
]


if __name__ == '__main__':
    pass