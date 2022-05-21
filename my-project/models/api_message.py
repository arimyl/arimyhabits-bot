import dataclasses
from datetime import datetime
import time
import uuid

import google.cloud.firestore as g_firestore

from modules.nanoseconds import datetime_with_nanoseconds


@dataclasses.dataclass
class ApiMessages():
    message: str
    
    def set_message(self, collection: g_firestore):
        collection.document().set({
            'id': str(uuid.uuid4()),
            'message': self.message,
            'timestamp': datetime_with_nanoseconds(datetime.fromtimestamp(round(time.time())))
        })