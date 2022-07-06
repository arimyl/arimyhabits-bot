from enum import Enum
from typing import List

from linebot.models import TemplateSendMessage, ConfirmTemplate, ButtonsTemplate


class MessageType(Enum):
    confirm = 1
    button = 2


def compose_template_message(
    type_obj: MessageType, text: str, conversation_types: List[dict] = None
) -> TemplateSendMessage:
    """TemplateMessageの選択"""
    if type_obj == MessageType.confirm:
        template = ConfirmTemplate(text, confirm_actions)
    elif type_obj == MessageType.button:
        template = ButtonsTemplate(
            text, actions=compose_type_button(conversation_types)
        )
    else:
        # template
        return

    return TemplateSendMessage("this is a template", template)


def compose_type_button(types: List[dict]) -> List[dict]:
    """typesからbutton actionを作成
    :types: type of text message.
    :return [button_action, ...]
    """
    if types is None:
        types = []

    buttons_actions = []
    for t in types:
        action = {"type": "message", "label": t["name"], "text": str(t["number"])}
        buttons_actions.append(action)
    buttons_actions.append({"type": "message", "label": "新規追加", "text": "0"})

    return buttons_actions


confirm_actions = [
    {"type": "message", "label": "はい", "text": "はい"},
    {"type": "message", "label": "いいえ", "text": "いいえ"},
]
