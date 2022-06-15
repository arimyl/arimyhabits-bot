import dataclasses
from datetime import datetime
import time
import uuid

import google.cloud.firestore as g_firestore

from modules.nanoseconds import datetime_with_nanoseconds


_id = "id"
_message_ids = "message_ids"
_timestamp = "timestamp"
_conversation_type = "conversation_type"


@dataclasses.dataclass
class ApiConversation:
    id: str = str(uuid.uuid4())
    message_ids: list = []
    conversation_type: int = 0

    def register_conversation(self, collection: g_firestore, message_id: str) -> None:
        msg_ids = self.message_ids
        if not (msg_ids):
            return None

        collection.document().set(
            {
                _id: self.id,
                _message_ids: msg_ids.append(message_id),
                _timestamp: datetime_with_nanoseconds(
                    datetime.fromtimestamp(round(time.time()))
                ),
                _conversation_type: self.conversation_type,
            }
        )

    def update_conversation(
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
                _conversation_type: self.conversation_type,
            }
        )

    def select_conversation_type(self, num: int):
        self.conversation_type = num
