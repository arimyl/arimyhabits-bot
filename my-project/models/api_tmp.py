import dataclasses
from datetime import datetime
import time

import google.cloud.firestore as g_firestore

from modules.nanoseconds import datetime_with_nanoseconds


_message_ids = "message_ids"
_timestamp = "timestamp"
_type_number = "type_number"


@dataclasses.dataclass
class ApiTmporary:
    message_ids: list = []
    type_number: int = 0

    def set_temporary(self, collection: g_firestore, message_id: str) -> None:
        msg_ids = self.message_ids
        if not (msg_ids):
            return None

        collection.document().set(
            {
                _message_ids: msg_ids.append(message_id),
                _timestamp: datetime_with_nanoseconds(
                    datetime.fromtimestamp(round(time.time()))
                ),
                _type_number: self.type_number,
            }
        )

    def update_temporary(
        self, collection: g_firestore, doc_id: str, message_id: str
    ) -> None:
        msg_ids = self.message_ids
        if not (msg_ids):
            return None

        collection.document(doc_id).update(
            {
                _message_ids: self.message_ids.append(message_id),
                _timestamp: datetime_with_nanoseconds(
                    datetime.fromtimestamp(round(time.time()))
                ),
                _type_number: self.type_number,
            }
        )

    def select_type_number(self, num: int):
        self.type_number = num
