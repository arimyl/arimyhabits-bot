from typing import  List

from linebot.models import (
    TemplateSendMessage,
    ConfirmTemplate, ButtonsTemplate
)


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
            'label': i['name'],
            'text': i['number']
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