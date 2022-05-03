from heapq import merge
from typing import List

from firebase_admin import firestore
import google.cloud.firestore as g_firestore

from models.api_message import ApiMessages
from settings.firebase_init import firebase_app


def register_message(message: str, user: str='test_user') -> None:
    """messageをFirestoreに登録する"""
    messages = ApiMessages(message)
    coll = connect_collection()
    messages.set_message(coll.document(user).collection('messages'))


def register_tmp(message: str, user: str='test_user') -> None:
    """messageをFirestoreに登録する"""
    messages = ApiMessages(message)
    collection = connect_collection()
    messages.set_message(collection.document(user).collection('messages'))


def connect_collection(root_collection: str='arihabits') -> g_firestore.CollectionReference:
    db = firestore.client(firebase_app())
    return db.collection(root_collection)


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


def update_user_info(collection: g_firestore.CollectionReference, user='test_user'):
    param = {
        'timestamp': firestore.SERVER_TIMESTAMP
    }
    collection.document(user).update(param)


def set_user_summary(collection: g_firestore.CollectionReference, param: dict, user='test_user'):
    summary_coll = collection.document(user).collection('summary')
    if len(param.keys()) == 5:
        # repair-point
        set_param = {
            'data_name': param['data_name'],
            'type': param['type'],
            'count': param['count'],
            'detail': param['detail'],
            'birthday': param['birthday']
        }
        summary_coll.document().set(set_param)
    elif len(param.keys()) > 0:
        result = summary_coll.where('data_name', '==', param['data_name']).stream()
        for snap in result:
            doc_id = snap.id
            summary_coll.document(doc_id).set(param, {merge: True})


def get_message_types(user: str='test_user') -> List[dict]:
    """Firestoreからメッセージの種類一覧を取得する
    :user str: user Document name
    """
    types_coll = connect_collection().document(user).collection('types')
    return [doc.to_dict() for doc in types_coll.stream()]


def get_document_id():
    collection = connect_collection()
    user_name = 'test_user'
    collection.where(
        __name__,
        '==',
        user_name
    )


if __name__ == '__main__':
    # messages = ApiMessages('Test message', 1)
    # messages.connect_message_collection()
    # messages.set_message()
    # for doc in messages.get_messages():
    #     print(doc.to_dict())

    # line = LINEUser.from_kwargs(**{'user_id':'id2', 'user_name':'name2','tes1':'aa','tes2':'bb'})
    # print(line.tes1)
    
    # source = get_users_info(col)
    # for doc in source:
    #     print(doc.to_dict())
    #     print(doc.id)
    #     update_user_info(user=doc.id)
    pass