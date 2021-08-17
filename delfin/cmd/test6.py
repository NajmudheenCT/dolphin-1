import datetime, pytz
from tzlocal import get_localzone


def get_timestamp_offset_from_utc_ms():
    TIME_ZONE = 'Pacific/Kwajalein'

    timez = get_localzone()
    if TIME_ZONE != 'local':
        timez = pytz.timezone("Atlantic/Bermuda")
    timez.utcoffset(datetime.datetime.now())
    return int(timez.utcoffset(datetime.datetime.now()).total_seconds() * 1000)


print(get_timestamp_offset_from_utc_ms() + 1)
