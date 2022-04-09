import dataclasses
from datetime import datetime, timezone
from heapq import merge
from inspect import signature
import json
import time
from typing import List

from firebase_admin import firestore
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import google.cloud.firestore 

from firebase_init import firebase_app


def nanoseconds_to_datetime(value:float) -> datetime:
    datetime.fromtimestamp(value.timestamp(), tz=timezone.utc)

def datetime_with_nanoseconds(dt:datetime=0) -> DatetimeWithNanoseconds:
    """Create <Firestore timestamp>"""
    if dt == 0:
        dt = datetime.now(tz=timezone.utc)
    dtnanos = DatetimeWithNanoseconds(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond,
        tzinfo=timezone.utc
    )
    return dtnanos

@dataclasses.dataclass
class ApiMessages():
    message: str
    type: int
    timestamp: int = round(time.time())
    
    def connect_message_collection(self, db:google.cloud.firestore=firestore.client(firebase_app()), root_collection='arihabits', user='test_user'):
        self.collection = db.collection(root_collection).document(user).collection('messages')

    def get_messages(self) -> List[dict]:
        self.messages = self.collection.stream()
        return self.messages

    def set_message(self):
        self.collection.document().set({
            'message': self.message,
            'type': self.type,
            'timestamp': datetime_with_nanoseconds(datetime.fromtimestamp(self.timestamp))
        })

@dataclasses.dataclass
class LINEUser:
    user_id: str
    user_name: str

    @classmethod
    def from_kwargs(cls, **kwargs):
        # cls.__dataclass_fields__.keys()
        # fetch the constractor's signature
        cls_fields = {fields for fields in signature(cls).parameters}

        # split the keargs into native ones and new ones
        native_args, new_args = {}, {}
        for name, val in kwargs.items():
            if name in cls_fields:
                native_args[name] = val
            else:
                new_args[name] = val
        
        # use the native ones to create the class ...
        ret = cls(**native_args)
        # ... and add the new ones by hand 
        for new_name, new_val in new_args.items():
            setattr(ret, new_name, new_val)
        return ret

def connect_collection(root_collection:str='arihabits') -> google.cloud.firestore.CollectionReference:
    db = firestore.client(firebase_app())
    return db.collection(root_collection)

def get_users_info(collection:google.cloud.firestore.CollectionReference, conditions:List[str]='') -> List:
    if conditions == '':
        return collection.stream()
    elif len(conditions) == 3:
        return collection.where(conditions[0],conditions[1],conditions[2]).stream()
    else:
        return list()

def update_user_info(collection:google.cloud.firestore.CollectionReference, user='test_user'):
    param = {
        'timestamp': firestore.SERVER_TIMESTAMP
    }
    collection.document(user).update(param)

def set_user_summary(collection:google.cloud.firestore.CollectionReference, param:dict, user='test_user'):
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


def get_profile(line_bot_api:object, user_id:str):
    """プロフィールを取得する
    """
    profile = line_bot_api.get_profile(user_id) # json
    profile_dict = json.loads(profile) # dict
    display_name = profile_dict['displayName']
    language = profile_dict['language']
    status_message = profile_dict['statusMessage']
    user_obj = LINEUser(user_id, display_name)
    # register_message(status_message, 0)

if __name__ == '__main__':
    # messages = ApiMessages('Test message', 1)
    # messages.connect_message_collection()
    # messages.set_message()
    # for doc in messages.get_messages():
    #     print(doc.to_dict())

    # line = LINEUser.from_kwargs(**{'user_id':'id2', 'user_name':'name2','tes1':'aa','tes2':'bb'})
    # print(line.tes1)
    coll = connect_collection()    
    
    # source = get_users_info(col)
    # for doc in source:
    #     print(doc.to_dict())
    #     print(doc.id)
    #     update_user_info(user=doc.id)