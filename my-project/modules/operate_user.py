from firebase_admin import firestore

import models.api_user
from modules.operate_firebase import (
    connect_collection,
    register_document,
    search_collectionDocuments,
)


def confirm_user(user_id: str):
    """confirm registered user whether or not.
    :user_id: line user_id
    """
    user_info = get_user_info_from_user_id(user_id)
    if user_info is None:
        user_name = ""
        register_user(user_name, user_id)
    else:
        print(f"{user_info.id}:", user_info.to_dict())  #


def get_user_info_from_user_id(user_id: str) -> dict:
    conditions = ["user_id", "==", user_id]
    users_info = search_collectionDocuments(connect_collection(), conditions)

    user_info_list = [_ for _ in users_info]
    if len(user_info_list) == 1:
        return user_info_list[0]
    return None


def register_user(name: str, id: str):
    """register user for firestore"""
    params = models.api_user.set_user(name, id)
    register_document(connect_collection(), params)


def update_user_info(doc_id: str = "test_user", **kargs):
    """update user for firestore"""
    param = {
        models.api_user._password: models.api_user.make_user_password(),
        models.api_user._timestamp: firestore.SERVER_TIMESTAMP,
    }
    name = kargs.get(models.api_user._user_name)
    if name:
        param.update({models.api_user._user_name: name})

    coll = connect_collection()
    coll.document(doc_id).update(param)
