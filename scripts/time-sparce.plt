set terminal pngcairo transparent enhanced font "arial,14" 
#set terminal postscript eps  font "Times-Roman,12" #color
set output "graph/comp-time-sparse-datasets.png"

set ylabel "Time (sec, logscale)"
set xlabel "Variation of JMAX"
set logscale y

set format y "10^{%L}"
set xtics ("0.1" 1, "0.2" 2, "0.25" 3, "0.3" 4, "0.35" 5, "0.4" 6, "0.45" 7, "0.5" 8, "0.6" 9, "0.7" 10, "0.1" 11, "0.2" 12, "0.25" 13, "0.3" 14, "0.35" 15, "0.4" 16, "0.45" 17, "0.5" 18, "0.6" 19, "0.7" 20, "0.1" 21, "0.2" 22, "0.25" 23, "0.3" 24, "0.35" 25, "0.4" 26, "0.45" 27, "0.5" 28, "0.6" 29, "0.7" 30, "0.1" 31, "0.2" 32, "0.25" 33, "0.3" 34, "0.35" 35, "0.4" 36, "0.45" 37, "0.5" 38, "0.6" 39, "0.7" 40)

set xtics border in scale 0,0 nomirror rotate by -90 offset character 0, 0, 0 font "arial,11"
set x2tics ("MUSHROOM-5" 4.0, "RETAIL-5" 14.0, "T10I4D100K-5" 24.0, "T40I4D100K-5" 34.0) out nomirror
set x2tics border in scale 0,0 nomirror rotate by 0 offset character 0, 0, 0 font "arial,10"

set key inside center top  vertical Left reverse enhanced noautotitles box

set xrange [0.5:41.0]
set x2range [0.5:41.0]
set yrange [50:*]
#set ytics 0,200,3000

set style line 1 lt 0 lw 3 linecolor rgb "black"

set arrow from 10.5,1 to 10.5,1e5 nohead ls 1
set arrow from 20.5,1 to 20.5,1e5 nohead ls 1
set arrow from 30.5,1 to 30.5,1e5 nohead ls 1
set arrow from 40.5,1 to 40.5,1e5 nohead ls 1

plot \
"graph/mushroom/mushroom_CPU.txt" u 2:4 w lp lw 1 lt 1 pt 3 ps 1.2 t "ClosedDiv - MINCOV",\
"graph/mushroom/mushroom_CPU.txt" u 2:5 w lp lw 1 lt 2 pt 6 ps 1.2 t "ClosedDiv - FIRSTWITCOV",\
"graph/retail/retail_CPU.txt" u ($2+10):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/retail/retail_CPU.txt" u ($2+10):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/T10I4D100K/T10I4D100K_CPU.txt" u ($2+20):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/T10I4D100K/T10I4D100K_CPU.txt" u ($2+20):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/T40I10D100K/T40I10D100K_CPU.txt" u ($2+30):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/T40I10D100K/T40I10D100K_CPU.txt" u ($2+30):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle
