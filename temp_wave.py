import time
import datetime
# Module for activating GPIO pins (light sensor)
import RPi.GPIO as GPIO
# Module for display
from Adafruit_LED_Backpack import AlphaNum4
# Module for temperature sensor
from temp_sensor import read_temp

######### Sensitivity and setup #################

# No of values to use as average
n_ldr = 10
# Threshold for cummulative light change (% of avg)
ldr_avg_cumul_diff_threshold = 0.09
# Upper limit for light change (% of avg)
ldr_avg_diff_limit = 0.05
# Threshold for No of consecutive increases
n_increases_threshold = 5
# Refresh cumululative difference time (in seconds)
t_refresh = 3
# Light threshold. So that the display is not on at night
ldr_threshold = 1000
# Time for which to display temperature (seconds)
display_t = 5
# Minute at which a message will be displayed
minute = 30
# The minute message
min_msg = "This is the minute message"

# Initialise LDR variables.
ldr_reads = [0]*n_ldr
ldr_avg_cumul_diff = 0
ldr_avg_diff = 0
ldr_avg = 0
n_increases = 0
# Initialise file for writting ldr readings
directory='logs/'
filename=directory + 'ldr_readings'

def read_LDR(drain=0.1):
    """Measure time needed to charge the capacitor in ldr circuit. Small
    numbers mean lots of light and large numbers mean less light."""
    GPIO.setup(PinLDR, GPIO.OUT)
    GPIO.output(PinLDR, GPIO.LOW)
    time.sleep(drain) # Drains all charge from the capacitor
    charge_time = time.time()
    GPIO.setup(PinLDR, GPIO.IN) # Sets the pin to be input
    while True:
        if (GPIO.input(PinLDR) == GPIO.HIGH):
            charge_time = time.time() - charge_time
            break
    # It takes about 1 ms to charge in day light
    return charge_time*1000

def write_temp(duration=10):
    """Display the temperature for t seconds"""    
    t = read_temp()
    display.clear()
    display.print_float(t,decimal_digits=1,justify_right=False)
    display.print_str('C',justify_right=True)
    display.write_display()
    time.sleep(duration)
    display.clear()
    display.write_display()

def write_long_str(message,t=0.3,justify_right=False):
    """Write a message of arbitrary length. Refresh rate is set by
    variable t"""    
    pos=0
    while pos < len(message)+1:
        display.clear()
        display.print_str(message[pos:min(pos+4,len(message))],justify_right)
        display.write_display()
        pos += 1
        time.sleep(t)

def writeToFile(string, filename):
    pass
#    f = open(filename,'a')
#    f.write(string+'\n')
#    f.close

def calc_average(list):
    sum=0
    for ele in list: sum += ele
    return sum/len(list)

def refresh_readings(reads):
    for i in xrange(len(reads)-2,-1,-1):  reads[i] = read_LDR(ldr_drain)
    global ldr_avg
    ldr_avg = calc_average(reads)
    global ldr_avg_cumul_diff
    ldr_avg_cumul_diff = 0
    global n_increases
    n_increases = 0
        
def minute_message():
    """The message to be displayed every some minutes"""
    print("Displaying minute message")
    write_long_str(min_msg)
    write_temp(10)

#########################################################
# Configuration (Do not change)                         #
# Set the GPIO Mode which is used by the light sensor   #
GPIO.setmode(GPIO.BCM)                                  #
GPIO.setwarnings(False)                                 #
# A variable with the LDR reading pin number            #
PinLDR = 27                                             #
# Time delay to let the capacitor charge drain          #
ldr_drain = 0.03                                        #
# Initialise display                                    #
display = AlphaNum4.AlphaNum4()                         #
display.begin()                                         #
display.set_brightness(15)                              #
#########################################################

open(filename,'w').close
writeToFile('# Readings from the LDR circuit ',filename)
writeToFile('# Scaled Readings \t Moving average \t Scaled Avg cumulative difference \t Scaled Avg difference',filename)
writeToFile('# Scaled variables are divided with value of moving average.',filename)
first=True

while True:
    try:
        ldr_reads.insert(0,read_LDR(ldr_drain))
        del ldr_reads[n_ldr]
        # Reset ldr_avg_cumul_diff to 0 every t_refresh (otherwise it deviates)
        if (ldr_avg_cumul_diff != 0 and datetime.datetime.now().second % t_refresh == 0):
            ldr_avg_cumul_diff=0
        # Turn off if dark (for 10 minutes)
        if  ldr_reads[0] > ldr_threshold:
            pause_message = "# Paused. LDR read: "+str(round(ldr_reads[0],3))
            writeToFile(pause_message, filename)
            print(pause_message)
            time.sleep(600)
            first=True # To go through refreshing when it wakes
        else:
            # First message
            if first:
                minute_message()
                first=False
                # Get fresh readings
                refresh_readings(ldr_reads)
            else:
                ldr_avg_prev = ldr_avg
                ldr_avg = calc_average(ldr_reads)
                ldr_avg_cumul_diff += ldr_avg - ldr_avg_prev
                ldr_avg_diff = ldr_avg - ldr_avg_prev
                # Monitor sequential increases used for the trigger criterion
                if (ldr_avg - ldr_avg_prev > 0): n_increases+=1
                else: n_increases=0
                writeToFile( str(ldr_reads[0]/ldr_avg)+" "+str(ldr_avg)+" "+str(ldr_avg_cumul_diff/ldr_avg)+" "+str(ldr_avg_diff/ldr_avg), filename)
                # Refresh if large jumps are detected (avoids accidental triggers)
                if ( ldr_avg_diff/ldr_avg > ldr_avg_diff_limit ):
                    refresh_readings(ldr_reads)
                    continue
                # Trigger criterion
                trigger = ldr_avg_cumul_diff/ldr_avg > ldr_avg_cumul_diff_threshold and n_increases > n_increases_threshold
                if ( trigger ):
                    print("Displaying temperature "+datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
                    display.clear()
                    display.print_str("Hey")
                    display.write_display()
                    write_temp(display_t)
                    refresh_readings(ldr_reads)
                elif (datetime.datetime.now().minute % minute == 0 and datetime.datetime.now().second < 10):
                    minute_message()
    except IOError as e:
        display.clear()
        display.write_display()
        print("IO error({0}): {1}".format(e.errno, e.strerror))
        continue
    except KeyboardInterrupt:
        display.clear()
        display.write_display()
        GPIO.cleanup()    
        print("\nExited after catching ctrl-c signal")
        exit()

