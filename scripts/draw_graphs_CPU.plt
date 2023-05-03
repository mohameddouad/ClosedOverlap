#set terminal pngcairo transparent enhanced font "arial,6" 
set terminal postscript eps 11 #color
set output "graph/CPU.eps"

set ylabel "CPU time in seconds"
set xlabel "Variation of JMAX"

set format y "10^{%L}"
set xtics ("0.1" 1, "0.2" 2, "0.25" 3, "0.3" 4, "0.35" 5, "0.4" 6, "0.45" 7, "0.5" 8, "0.6" 9, "0.7" 10, "0.1" 11, "0.2" 12, "0.25" 13, "0.3" 14, "0.35" 15, "0.4" 16, "0.45" 17, "0.5" 18, "0.6" 19, "0.7" 20, "0.1" 21, "0.2" 22, "0.25" 23, "0.3" 24, "0.35" 25, "0.4" 26, "0.45" 27, "0.5" 28, "0.6" 29, "0.7" 30, "0.1" 31, "0.2" 32, "0.25" 33, "0.3" 34, "0.35" 35, "0.4" 36, "0.45" 37, "0.5" 38, "0.6" 39, "0.7" 40, "0.1" 41, "0.2" 42, "0.25" 43, "0.3" 44, "0.35" 45, "0.4" 46, "0.45" 47, "0.5" 48, "0.6" 49, "0.7" 50, "0.1" 51, "0.2" 52, "0.25" 53, "0.3" 54, "0.35" 55, "0.4" 56, "0.45" 57, "0.5" 58, "0.6" 59, "0.7" 60, "0.1" 61, "0.2" 62, "0.25" 63, "0.3" 64, "0.35" 65, "0.4" 66, "0.45" 67, "0.5" 68, "0.6" 69, "0.7" 70)

set xtics border in scale 0,0 nomirror rotate by -90 offset character 0, 0, 0 font "arial,6"
set x2tics ("hepatitis" 4.0, "mushroom" 14.0, "pumsb" 24.0,"retail" 34.0, "T10I4D100K" 44.0, "connect" 54.0, "kr-vs-kp" 64.0) out nomirror
set x2tics border in scale 0,0 nomirror rotate by 45 offset character 0, 0, 0 font "arial,6"

set key inside right bottom vertical Left reverse enhanced noautotitles box

set xrange [0.5:100.0]
set x2range [0.5:100.0]
set yrange [-100:*]

set style line 1 lt 0 lw 3 linecolor rgb "black"

set arrow from 10.5,1 to 10.5,1e5 nohead ls 1
set arrow from 20.5,1 to 20.5,1e5 nohead ls 1
set arrow from 30.5,1 to 30.5,1e5 nohead ls 1
set arrow from 40.5,1 to 40.5,1e5 nohead ls 1
set arrow from 50.5,1 to 50.5,1e5 nohead ls 1
set arrow from 60.5,1 to 60.5,1e5 nohead ls 1
set arrow from 70.5,1 to 70.5,1e5 nohead ls 1

plot \
"graph/hepatitis/hepatitis_CPU.txt" u 2:4 w linespoints linecolor rgb "red" pt 3 ps 0.8 title "ClosedDiv - MINCOV",\
"graph/hepatitis/hepatitis_CPU.txt" u 2:5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 title "ClosedDiv - FIRSTWITCOV",\
"graph/mushroom/mushroom_CPU.txt" u ($2+10):4 w linespoints linecolor rgb "red" pt 3 ps 0.8 notitle,\
"graph/mushroom/mushroom_CPU.txt" u ($2+10):5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 notitle,\
"graph/pumsb/pumsb_CPU.txt" u ($2+20):4 w linespoints linecolor rgb "red" pt 3 ps 0.8 notitle,\
"graph/pumsb/pumsb_CPU.txt" u ($2+20):5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 notitle,\
"graph/retail/retail_CPU.txt" u ($2+30):4 w linespoints linecolor rgb "red" pt 3 ps 0.8 notitle,\
"graph/retail/retail_CPU.txt" u ($2+30):5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 notitle,\
"graph/connect/connect_CPU.txt" u ($2+40):4 w linespoints linecolor rgb "red" pt 3 ps 0.8 notitle,\
"graph/connect/connect_CPU.txt" u ($2+40):5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 notitle,\
"graph/T10I4D100K/T10I4D100K_CPU.txt" u ($2+50):4 w linespoints linecolor rgb "red" pt 3 ps 0.8 notitle,\
"graph/T10I4D100K/T10I4D100K_CPU.txt" u ($2+50):5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 notitle,\
"graph/kr-vs-kp/kr-vs-kp_CPU.txt" u ($2+60):4 w linespoints linecolor rgb "red" pt 3 ps 0.8 notitle,\
"graph/kr-vs-kp/kr-vs-kp_CPU.txt" u ($2+60):5 w linespoints linecolor rgb "blue" pt 7 ps 0.8 notitle
