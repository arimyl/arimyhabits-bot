import dataclasses
from datetime import datetime, timezone
import time
import uuid

from google.api_core.datetime_helpers import DatetimeWithNanoseconds
import google.cloud.firestore as g_firestore


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
    timestamp: int = round(time.time())
    
    def set_message(self, collection: g_firestore):
        collection.document().set({
            'id': str(uuid.uuid4()),
            'message': self.message,
            'timestamp': datetime_with_nanoseconds(datetime.fromtimestamp(self.timestamp))
        })