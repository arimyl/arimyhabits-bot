develop = True  # flag

from heapq import merge
from typing import List

from firebase_admin import firestore
import google.cloud.firestore as g_firestore

if develop:
    from settings.firebase_init_develop import firebase_app
else:
    from settings.firebase_init import firebase_app


def connect_collection(
    root_collection: str = "arihabits",
) -> g_firestore.CollectionReference:
    db = firestore.client(firebase_app())
    return db.collection(root_collection)


def register_document(collection, params) -> None:
    """"""
    collection.document().set(params)


def search_collectionDocuments(
    collection: g_firestore.CollectionReference, conditions: List[str]
) -> object:
    """get users fields from firestore
    :conditions[0]: field name
    :conditions[1]: conditional expression
    :conditions[2]: field value
    """
    if conditions == "":
        return collection.stream()
    elif len(conditions) == 3:
        return collection.where(conditions[0], conditions[1], conditions[2]).stream()
    else:
        return list()


def set_user_summary(
    collection: g_firestore.CollectionReference, param: dict, doc_id="test_user"
):
    summary_coll = collection.document(doc_id).collection("summary")
    if len(param.keys()) == 5:
        # repair-point
        set_param = {
            "data_name": param["data_name"],
            "type": param["type"],
            "count": param["count"],
            "detail": param["detail"],
            "birthday": param["birthday"],
        }
        register_document(summary_coll, set_param)

    elif len(param.keys()) > 0:
        result = summary_coll.where("data_name", "==", param["data_name"]).stream()
        for snap in result:
            doc_id = snap.id
            summary_coll.document(doc_id).set(param, {merge: True})


def get_message_types(user: str = "test_user") -> List[dict]:
    """Firestoreからメッセージの種類一覧を取得する
    :user str: user Document name
    """
    types_coll = connect_collection().document(user).collection("types")
    return [doc.to_dict() for doc in types_coll.stream()]


def get_document_id():
    collection = connect_collection()
    user_name = "test_user"
    collection.where(__name__, "==", user_name)


if __name__ == "__main__":
    # source = get_users_info(col)
    # for doc in source:
    #     print(doc.to_dict())
    #     print(doc.id)
    #     update_user_info(user=doc.id)
    pass
