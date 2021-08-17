import datetime
from dateutil import tz
def convert_utc_to_local(utc):
    to_zone = tz.tzlocal()
    utc_c = float(utc.strftime("%s"))
    datetime_utc = datetime.datetime.fromtimestamp(utc_c)
    print(datetime_utc)
    # Convert time zone
    local_timez = datetime_utc.astimezone(to_zone)
    local_timestamp = int(local_timez.timestamp())
    print(local_timez)
    return local_timestamp
print(convert_utc_to_local(datetime.datetime.utcnow()))