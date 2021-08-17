from datetime import datetime

from dateutil import tz


def convert_utc_to_local_timestamp(utc):

    to_zone = tz.tzlocal()
    datetime_utc = datetime.fromtimestamp(utc / 1000)
    # Convert time zone
    local = datetime_utc.astimezone(to_zone)
    localtime = int(local.timestamp() * 1000)
    print(localtime)
convert_utc_to_local_timestamp(1623406241000)