from datetime import datetime, timezone

from google.api_core.datetime_helpers import DatetimeWithNanoseconds


def nanoseconds_to_datetime(value: float) -> datetime:
    datetime.fromtimestamp(value.timestamp(), tz=timezone.utc)


def datetime_with_nanoseconds(dt: datetime = 0) -> DatetimeWithNanoseconds:
    """Create <Firestore timestamp>
    :dt: default = 0. case of value is 0, time is now.
    """
    if dt == 0:
        dt = datetime.now(tz=timezone.utc)
    dtnanos = DatetimeWithNanoseconds(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond,
        tzinfo=timezone.utc,
    )
    return dtnanos
