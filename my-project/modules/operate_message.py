import models.api_message
from modules.operate_firebase import (
    connect_collection,
    register_document,
    search_collectionDocuments,
)


def register_message(message: str, user_docId: str = "test_user") -> str:
    """messageをFirestoreに登録する
    return
    ---------
    id str: message id(uuid4)
    """
    msg_coll = _messages_collection(user_docId)
    params = models.api_message.create_message(message)
    register_document(msg_coll, params)
    return params[models.api_message._id]


def _messages_collection(user_docId):
    return connect_collection().document(user_docId).collection("messages")


def get_message(user_docId: str, id: str):
    conditions = [models.api_message._id, "==", id]
    coll = _messages_collection(user_docId)
    search_collectionDocuments(coll, conditions)
