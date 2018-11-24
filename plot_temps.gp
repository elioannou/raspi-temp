# Plot temperatures

filename="logs/temps_raw_data"
stats filename using 1 

set ylabel "Temperature [^{o}C]"
set ytics 0.5
set y2tics 0.5

set term svg size 1920,900 font ",20" enhanced
set output 'temps.svg'

# Gnuplot can plot date and time but you need to specify
set xdata time
# Specify what format the date/time is in the input file
set timefmt "%d-%m-%Y\t%H:%M:%S"
# Set the format at which date time will be labeled on axis
set format x "%H:%M\n%d-%m"
# Set range
daysback=2
secondsago = strftime("%d-%m-%Y\t%H:%M:%S", time(0)-60*60*24*daysback ) # Note: Time function returns UTC
set xrange [secondsago:]

set grid

set style fill transparent solid 0.2 noborder
error = 0.3
plot filename u 1:($3-error):($3+error) w filledcurves ls 1 title '-/+ 0.3', filename using 1:3 w lp pt 7 ps 0.5 lc 1 lw 1.5 notitle

unset output

set output 'temps_day_comparison.svg'

set xdata time
# Specify what format the date/time is in the input file
set timefmt "%H:%M:%S"
# Set the format at which date time will be labeled on axis
set format x "%H:%M"
set xrange ["00:00":"24:00"]

idx=STATS_blocks-1
print idx
if ( idx < 2) {
daysback=idx
}
else {
daysback=2
}

set style fill transparent solid 0.2 noborder
error = 0.3
titles = "Today Yesterday Day-before-yesterday"
plot for [i=0:daysback] filename index idx-i u 2:($3-error):($3+error) w filledcurves ls 1+i notitle, \
     for [i=0:daysback] filename index idx-i using 2:3 w lp pt 7 ps 0.5 lc 1+i lw 1.5 title word(titles,i+1)


unset output
