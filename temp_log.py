import time
import datetime
import os

from temp_sensor import read_temp

def writeToFile(string, filename):
    f = open(filename,'a')
    f.write(string+'\n')
    f.close

def current_datetime():
    return datetime.datetime.now().strftime('%d-%m-%Y\t%H:%M:%S')

start_datetime = current_datetime()
#start_date = datetime.datetime.now().strftime('%d-%m-%Y')
directory='/home/schlang/projects/temperature/logs/'
filename=directory + 'temps_raw_data' #+ start_date
if not (os.path.exists(filename)):
    writeToFile('# Temperatures started on ' + start_datetime,filename)
    writeToFile('# Date [dd-mm-yyyy]\t Time [hh:mm]\t Temperature [C] ',filename)

try: 
    writeToFile(current_datetime() + "\t" + str(read_temp()),filename)


except KeyboardInterrupt:
    print("\nExited after catching ctrl-c")
except IOError as e:
    print("IO error({0}): {1}".format(e.errno, e.strerror))
