import re
import uuid

from modules.nanoseconds import datetime_with_nanoseconds


_user_name = "user_name"
_user_id = "user_id"
_password = "password"
_timestamp = "timestamp"


def set_user(name: str, id: str) -> dict:
    return {
        _user_name: name,
        _user_id: id,
        _password: make_user_password(),
        _timestamp: datetime_with_nanoseconds(),
    }


def make_user_password() -> str:
    return re.sub(r"-", "", str(uuid.uuid4()))[::8]
