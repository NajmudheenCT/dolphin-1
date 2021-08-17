import glob
import os

# Path
import time


def get_file_or_folder_age(path):
    # getting ctime of the file/folder
    # time will be in seconds
    ctime = os.stat(path).st_ctime

    # returning the time
    return ctime



# files = glob.glob("/var/lib/delfin/metrics/*.prom.temp")
# files.sort(key=os.path.getmtime)
# print("\n".join(files))
files = glob.glob("/var/lib/delfin/metrics/*.prom")
for file in files:
    print(get_file_or_folder_age(file))
    seconds = time.time() - 3600
print(seconds)
