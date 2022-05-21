import re
import uuid

from modules.nanoseconds import datetime_with_nanoseconds


_user_name = 'user_name'
_user_id = 'user_id'
_password = 'password'
_timestamp = 'timestamp'


class ApiUser:
    pass


def compose_user(name: str, id: str) -> dict:
    return {
        _user_name: name,
        _user_id: id,
        _password: re.sub(r'-', '',str(uuid.uuid4()))[::8],
        _timestamp: datetime_with_nanoseconds()
    }
