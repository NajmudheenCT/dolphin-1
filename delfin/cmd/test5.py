import datetime as dt
import pytz
from tzlocal import get_localzone # $ pip install tzlocal


def tz_from_utc_ms_ts(utc_ms_ts, tz_info):
    """Given millisecond utc timestamp and a timezone return dateime

    :param utc_ms_ts: Unix UTC timestamp in milliseconds
    :param tz_info: timezone info
    :return: timezone aware datetime
    """
    # convert from time stamp to datetime
    utc_datetime = dt.datetime.utcfromtimestamp(utc_ms_ts / 1000.)

    # set the timezone to UTC, and then convert to desired timezone
    return utc_datetime.replace(tzinfo=pytz.timezone('UTC')).astimezone(tz_info)

utc_ts = 1623657238000
tz = get_localzone().__str__()
print(tz)
tz_dt = tz_from_utc_ms_ts(utc_ts, pytz.timezone(tz))

print(tz_dt)
print(tz_dt.strftime('%d-%m-%Y'))
