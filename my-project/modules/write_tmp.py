from datetime import datetime as dt
import os
import pathlib as path
from typing import List

import google.cloud.firestore as g_firestore

from modules.operate_firebase import connect_collection
from models.api_tmp import ApiTmporary


def register_tmp(message_id: str, doc_id: str = "test_user") -> None:
    """messageをFirestoreに登録する"""
    tmp = ApiTmporary()
    coll = connect_collection()
    tmp.set_temporary(coll.document(doc_id).collection("tmps"), message_id)


def get_tmp():
    pass


def update_tmp(collection: g_firestore.CollectionReference, doc_id="test_user"):
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
