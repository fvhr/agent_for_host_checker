import datetime

import pytz


def convert_to_moscow_time(value=None):
    moscow_tz = pytz.timezone('Europe/Moscow')
    if not value:
        value = datetime.datetime.now()
    if value is not None:
        if value.tzinfo is None:
            value = value.replace(tzinfo=pytz.utc)
        value = value.astimezone(moscow_tz)
        return value.replace(tzinfo=None)
    return None