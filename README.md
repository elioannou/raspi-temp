## Temperature logger and display

This project uses the raspberry pi along with other electronics to measure the
temperature, plot it in a website and show it on-demand on a LED alphanumeric
display.

![showcase](https://github.com/elioannou/raspi-temp/raw/master/showcase.gif)

### Hardware used

1. Raspberry Pi 3 Model B
2. Temperature sensor DS18B20
3. Light Dependent Resistor (LDR)
4. Capacitor (1 μF)
4. 0.54" Alphanumeric display and backpack from Adafruit
5. Wires and resistors for setting them up.

### Setup

The setup involves connecting the electronics, enable the appropriate interfaces
on the raspberry pi and running the python scripts.

The wiring of the circuits and connections to the raspberry pi is not covered
here.  
Guidelines can be found in:

1. [CamJam Edukit 2: Sensors](https://camjam.me/?page_id=623) for the temperature sensor and LDR circuits
2. [Adafruit](https://learn.adafruit.com/led-backpack-displays-on-raspberry-pi-and-beaglebone-black/wiring)
   for the LED backpack.
   
The interfaces used are the 1-wire for the temperature sensor and the I2C for the
alphanumeric display. Guidelines on how to enable them are also found in the
links given above.

The last step is running two python scripts with information given in the
following sections. Because of dependency on some libraries, python 2 should be
used.

### Logger

The start logging run `python temp_logger.py`. This creates a file in the logs
directory with the date time and temperature value.

Alternatively, you can use the script `temp_log.py` which will log a single
measurement of temperature in the same file as the above logger. It's purpose is
to be used in a cronjob.

To plot temperatures use the gnuplot script `plot_temp.gp` which will output the
files in the `webpage` directory.

To access the website online you should make a symbolic link from the location where
websites are published in your system.  
e.g. `/var/www/html` in Debian  
You can also create a cron job to run the gnuplot script and plot the new values
of temperature.


### Display with hand wave

The code in `temp_wave` uses the LDR to detect a hand wave over the circuitry
and display the temperature.  
To initiate, run `python temp_wave.py`.

The LDR is an analog device and to convert its response to digital, we use a circuit
that charges a capacitor. We measure the time to charge the capacitor which
depends on the amount of light.

This method produces an unstable signal that makes it a challenge to find an
effective way of detecting the hand wave. Alternatively, an ADC can be used to
convert the analogue signal or a motion sensor which would provide more reliable
methods of detecting a hand motion.

Nevertheless, this project uses a few simple criteria to detect the hand wave
within the current setup. It calculates the rolling average of the time-to-charge
and the cumulative difference of each value with the previous. The temperature 
display is triggered when their ratio increases above a threshold and if the 
increase has happened smoothly.
