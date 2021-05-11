import datetime
from time import sleep

time1 = datetime.datetime.now()
sleep(10)
time2 = datetime.datetime.now()

print(time2-time1)