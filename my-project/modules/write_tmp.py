from datetime import datetime as dt
import os
import pathlib as path
from typing import List

import google.cloud.firestore as g_firestore

from modules.operate_firebase import connect_collection
from models.api_tmp import ApiTmporary


def get_user_info_from_user_id(user_id: str) -> dict:
    conditions = ['user_id', '==', user_id]
    users_info = get_users_info(connect_collection(), conditions)
    user_info_list = [_ for _ in users_info]
    # user_info_list = [a.to_dict() for a in get_users_info(coll, conditions)]
    if len(user_info_list) == 1:
        return user_info_list[0]
    return None


def get_users_info(collection: g_firestore.CollectionReference, conditions: List[str]='') -> object:
    """get users fields from firestore
    :conditions[0]: field name
    :conditions[1]: conditional expression
    :conditions[2]: field value
    """
    if conditions == '':
        return collection.stream()
    elif len(conditions) == 3:
        return collection.where(conditions[0],conditions[1],conditions[2]).stream()
    else:
        return list()


def register_tmp(message_id: str, user: str='test_user') -> None:
    """messageをFirestoreに登録する"""
    tmp = ApiTmporary()
    coll = connect_collection()
    tmp.set_temporary(coll.document(user).collection('tmps'), message_id)
        

def create_contents(message_text: str) -> List[list]:
    """"""
    contents = []
    for t in message_text.split(','):
        content = [t, str(dt.now())[:-3]]
        contents.append(content)
    return contents
