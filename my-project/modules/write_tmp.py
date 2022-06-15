from datetime import datetime as dt
from typing import List

from firebase_admin import firestore
import google.cloud.firestore as g_firestore

from modules.operate_firebase import connect_collection
from models.api_conversation import ApiConversation


def register_new_conversation(message_id: str, doc_id: str = "test_user") -> str:
    """messageをFirestoreに登録する
    return
    ----------
    id str: register collection of conversation id
    """
    conversation = ApiConversation()
    coll = connect_collection()
    conversation.register_conversation(
        coll.document(doc_id).collection("conversation"), message_id
    )
    return conversation._id


def get_conversation():
    pass


def update_conversation(
    collection: g_firestore.CollectionReference, doc_id="test_user"
):
    param = {"timestamp": firestore.SERVER_TIMESTAMP}
    collection.document(doc_id).update(param)
    pass


def create_contents(message_text: str) -> List[list]:
    """"""
    contents = []
    for t in message_text.split(","):
        content = [t, str(dt.now())[:-3]]
        contents.append(content)
    return contents
