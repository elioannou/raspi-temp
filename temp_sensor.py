# This file implements functions to read temperature for the
# temperature sensor. It should be included using "from
# temp_sensor import read_temp" and then use function
# read_temp() which returns a float value of temp in Celcius.

import os
import glob
import time

# Load required modules to the kernel
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

# Find the device file
device_dir = glob.glob('/sys/bus/w1/devices/28*')[0] # use first entry
device_file = device_dir + '/w1_slave'

# Extract text from device file
def read_temp_file():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_file()
    # If first line does not end in YES then wait and try again
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_file()

    # Find position of temperature in second line
    pos = lines[1].find('t=')

    # If position has been found convert temp to float and scale to
    # degrees celcius
    if pos !=-1:
        temp_string = lines[1][pos+2:]
        temp = float(temp_string) / 1000.0
        return temp
