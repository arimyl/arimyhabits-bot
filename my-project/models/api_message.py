from datetime import datetime
import time
import uuid

from modules.nanoseconds import datetime_with_nanoseconds


_id = "id"
_message = "message"
_timestamp = "timestamp"


def set_message(message: str) -> dict:
    return {
        _id: str(uuid.uuid4()),
        _message: message,
        _timestamp: datetime_with_nanoseconds(
            datetime.fromtimestamp(round(time.time()))
        ),
    }
