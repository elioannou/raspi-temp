import time
import datetime
import os

from temp_sensor import read_temp

# How often to log temperature (seconds)
interval=360 

def writeToFile(string, filename):
    f = open(filename,'a')
    f.write(string+'\n')
    f.close

def current_datetime():
    return datetime.datetime.now().strftime('%d-%m-%Y\t%H:%M:%S')

start_datetime = current_datetime()
#start_date = datetime.datetime.now().strftime('%d-%m-%Y')
directory='logs/'
filename=directory + 'temps_raw_data' #+ start_date
if os.path.exists(filename):
    ans=raw_input("ERROR: File "+filename+" already exists. Append? [Y/n] \n")
    if ( ans == 'n' or ans == 'no' or ans == 'N' or ans == 'No' ):
        open(filename,'w').close

# Interval in which measurements are logged (seconds)        
writeToFile('# Temperatures every '+ str(interval/60) +' minutes started on ' + start_datetime,filename)
writeToFile('# Date [dd-mm-yyyy]\t Time [hh:mm]\t Temperature [C] ',filename)
print('LOG: Temperature logging every ' +  str(interval/60) + ' minutes started on ' + start_datetime)
day = datetime.datetime.now().day

try: 
    while 1:
        today = datetime.datetime.now().day
        "Create new block if it is a new day"
        if  today != day:
            writeToFile("\n\n# New day: " + current_datetime(),filename)
            day = today
            
        writeToFile(current_datetime() + "\t" + str(read_temp()),filename)
        time.sleep(interval-1)

except KeyboardInterrupt:
    print("\nExited after catching ctrl-c")
except IOError as e:
    print("IO error({0}): {1}".format(e.errno, e.strerror))
