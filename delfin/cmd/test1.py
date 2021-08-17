import datetime

from dateutil import tz


def convert_utc_to_local(utc):
    to_zone = tz.tzlocal()
    datetime_utc = datetime.datetime.fromtimestamp(utc / 1000)
    # Convert time zone
    local_timez = datetime_utc.astimezone(to_zone)
    local_timestamp = int(local_timez.timestamp() * 1000)
    return local_timestamp


print(convert_utc_to_local(1623653899000))
