from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    ConfirmTemplate, ButtonsTemplate
)

from line_init import line_bot_api

def line_conversation(event):
    message_text = event.message.text
    if greeting(message_text): # 挨拶
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=message_text)]
        )
    elif message_text.isdigit(): # 数値
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(text=message_text),
                tmp_message('confirm', 'What number is this?')
            ]
        )
    
def greeting(message:str) -> str:
    """挨拶判定を行い、同じ挨拶を返す"""
    greetings = ['hello', 'おはよう', 'こんにちは','こんばんは']
    # greetings check
    if sum(list(map(lambda x: x in message.lower(), greetings))):
        return message
    return ''
        
def tmp_message(type:str, text:str) -> TemplateSendMessage:
    if type == 'confirm':
        tmp = ConfirmTemplate(
            text, confirm_actions
        )
    elif type == 'button':
        tmp = ButtonsTemplate(
            text, buttons_actions
        )
    else:
        tmp

    return TemplateSendMessage('this is a template', tmp)

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

buttons_actions = [
    {
        "type": "message",
        "label": "アクション 1",
        "text": "アクション 1"
    },
    {
        "type": "message",
        "label": "アクション 2",
        "text": "アクション 2"
    },
    {
        "type": "message",
        "label": "アクション 3",
        "text": "アクション 3"
    }
]

if __name__ == '__main__':
    pass