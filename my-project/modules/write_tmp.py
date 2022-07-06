from datetime import datetime as dt
from typing import List

from modules.operate_firebase import connect_collection
from models.api_conversation import ApiConversation


def register_new_conversation(message_id: str, user_id: str = "test_user") -> str:
    """messageをFirestoreに登録する
    return
    ----------
    id str: register collection of conversation id
    """
    conversation = ApiConversation()
    conversation.register_conversation(conversation_connect(user_id), message_id)
    return conversation._id


def get_conversation():
    pass


def update_conversation(doc_id: str, message_id: str, user_id="test_user"):
    conversation = ApiConversation()
    conversation.update_conversation(conversation_connect(user_id), doc_id, message_id)


def create_contents(message_text: str) -> List[list]:
    """"""
    contents = []
    for t in message_text.split(","):
        content = [t, str(dt.now())[:-3]]
        contents.append(content)
    return contents


def conversation_connect(doc_id: str):
    coll = connect_collection()
    return coll.document(doc_id).collection("conversation")
