# Plot temperatures

filename='< tail -n 100 logs/ldr_readings'

set term qt size 1200,675

set ylabel "Time [ms]"
set y2label "Diff"
set yrange [0:10]
set y2range [-0.15:0.15]
set ytics 1
set y2tics 0.03

set grid

plot filename u 1 w lp pt 3 title 'Scaled ldr value', filename u 2 w lp pt 3 title 'Rolling average', filename using 3 axis x1y2 w lp pt 4 title 'Scaled Avg Cumul Diff'

#pause 0.1
reread
#unset output
