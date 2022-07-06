from datetime import datetime
import time
import uuid
import dataclasses

from modules.nanoseconds import datetime_with_nanoseconds


@dataclasses.dataclass
class Message:
    id: str
    content: str
    timestamp: datetime

    def __init__(self, message):
        self.id = str(uuid.uuid4())
        self.content = message
        self.timestamp = datetime_with_nanoseconds(
            datetime.fromtimestamp(round(time.time()))
        )
