set terminal pngcairo transparent enhanced font "arial,12" 
#set terminal postscript eps  font "Times-Roman,12" #color
set output "graph/comp-time-dense-datasets.png"

set ylabel "Time (sec, logscale)"
set xlabel "Variation of JMAX"
set logscale y

set format y "10^{%L}"
set xtics ("0.1" 1, "0.2" 2, "0.25" 3, "0.3" 4, "0.35" 5, "0.4" 6, "0.45" 7, "0.5" 8, "0.6" 9, "0.7" 10, "0.1" 11, "0.2" 12, "0.25" 13, "0.3" 14, "0.35" 15, "0.4" 16, "0.45" 17, "0.5" 18, "0.6" 19, "0.7" 20, "0.1" 21, "0.2" 22, "0.25" 23, "0.3" 24, "0.35" 25, "0.4" 26, "0.45" 27, "0.5" 28, "0.6" 29, "0.7" 30, "0.1" 31, "0.2" 32, "0.25" 33, "0.3" 34, "0.35" 35, "0.4" 36, "0.45" 37, "0.5" 38, "0.6" 39, "0.7" 40, "0.1" 41, "0.2" 42, "0.25" 43, "0.3" 44, "0.35" 45, "0.4" 46, "0.45" 47, "0.5" 48, "0.6" 49, "0.7" 50)

set xtics border in scale 0,0 nomirror rotate by -90 offset character 0, 0, 0 font "arial,11"
set x2tics ("HEPATITIS-20" 4.0, "CHESS-40" 14.0, "CONNECT-40" 24.0, "HEART-CLEVELAND-20" 34.0, "KR-VS-KP-40" 44.0) out nomirror
set x2tics border in scale 0,0 nomirror rotate by 25 offset character 0, 0, 0 font "arial,10"

set key inside center bottom vertical Left reverse enhanced noautotitles box

set xrange [0.5:51.0]
set x2range [0.5:51.0]
set yrange [1:*]

set style line 1 lt 0 lw 3 linecolor rgb "black"

set arrow from 10.5,1 to 10.5,1e5 nohead ls 1
set arrow from 20.5,1 to 20.5,1e5 nohead ls 1
set arrow from 30.5,1 to 30.5,1e5 nohead ls 1
set arrow from 40.5,1 to 40.5,1e5 nohead ls 1
set arrow from 50.5,1 to 50.5,1e5 nohead ls 1


plot \
"graph/hepatitis/hepatitis_CPU.txt" u 2:4 w lp lw 1 lt 1 pt 3 ps 1.2 t "ClosedDiv - MINCOV",\
"graph/hepatitis/hepatitis_CPU.txt" u 2:5 w lp lw 1 lt 2 pt 6 ps 1.2 t "ClosedDiv - FIRSTWITCOV",\
"graph/chess/chess_CPU.txt" u ($2+10):4 w lp lw 1 lt 1 pt 3ps 1.2 notitle,\
"graph/chess/chess_CPU.txt" u ($2+10):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/connect/connect_CPU.txt" u ($2+20):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/connect/connect_CPU.txt" u ($2+20):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/heart-cleveland/heart-cleveland_CPU.txt" u ($2+30):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/heart-cleveland/heart-cleveland_CPU.txt" u ($2+30):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/kr-vs-kp/kr-vs-kp_CPU.txt" u ($2+40):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/kr-vs-kp/kr-vs-kp_CPU.txt" u ($2+40):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle
