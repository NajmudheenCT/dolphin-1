import os
from datetime import datetime

time_stamp = str(datetime.utcnow().timestamp())
temp_file_name = "/usr/naju/" + time_stamp + ".prom.temp"
actual_file_name = "/usr/naju/" + time_stamp + ".prom"
with open(temp_file_name, "w") as f:
    f.write("# HELP %s storage metric for %s\n" % (time_stamp, time_stamp))
    f.write("# TYPE %s gauge\n" % time_stamp)
    f.close()
    os.renames(temp_file_name,actual_file_name)
	# // write to the temp file
	# f, err := os.Create(tempFName)
	# if err != nil {
	# 	log.Error(err)
	# 	return
	# }
	# _, err = f.WriteString(finalString)
	# if err != nil {
	# 	log.Error(err)
	# 	f.Close()
	# 	return
	# }
	# log.Infof("metrics written successfully at time %s", timeStamp)
	# log.Infoln(finalString)
	# err = f.Close()
	# if err != nil {
	# 	log.Error(err)
	# 	return
	# }
	# // this is done so that the exporter never sees an incomplete file
	# renameErr := os.Rename(tempFName, fName)
	# if renameErr != nil {
	# 	log.Errorf("error %s renaming metrics file %s to %s", renameErr.Error(), tempFName, fName)
	# }