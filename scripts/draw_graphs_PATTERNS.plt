set terminal pngcairo transparent enhanced font "arial,11" 
#set terminal postscript eps  font "Times-Roman,12" #color
set output "graph/comp-patterns-datasets.png"

set ylabel "#Patterns (logscale)"
set xlabel "Variation de JMAX"
set logscale y

set format y "10^{%L}"

set xtics ("0.1" 1, "0.2" 2, "0.25" 3, "0.3" 4, "0.35" 5, "0.4" 6, "0.45" 7, "0.5" 8, "0.6" 9, "0.7" 10, "0.1" 11, "0.2" 12, "0.25" 13, "0.3" 14, "0.35" 15, "0.4" 16, "0.45" 17, "0.5" 18, "0.6" 19, "0.7" 20, "0.1" 21, "0.2" 22, "0.25" 23, "0.3" 24, "0.35" 25, "0.4" 26, "0.45" 27, "0.5" 28, "0.6" 29, "0.7" 30, "0.1" 31, "0.2" 32, "0.25" 33, "0.3" 34, "0.35" 35, "0.4" 36, "0.45" 37, "0.5" 38, "0.6" 39, "0.7" 40, "0.1" 41, "0.2" 42, "0.25" 43, "0.3" 44, "0.35" 45, "0.4" 46, "0.45" 47, "0.5" 48, "0.6" 49, "0.7" 50, "0.1" 51, "0.2" 52, "0.25" 53, "0.3" 54, "0.35" 55, "0.4" 56, "0.45" 57, "0.5" 58, "0.6" 59, "0.7" 60, "0.1" 61, "0.2" 62, "0.25" 63, "0.3" 64, "0.35" 65, "0.4" 66, "0.45" 67, "0.5" 68, "0.6" 69, "0.7" 70, "0.1" 71, "0.2" 72, "0.25" 73, "0.3" 74, "0.35" 75, "0.4" 76, "0.45" 77, "0.5" 78, "0.6" 79, "0.7" 80, "0.1" 81, "0.2" 82, "0.25" 83, "0.3" 84, "0.35" 85, "0.4" 86, "0.45" 87, "0.5" 88, "0.6" 89, "0.7" 90) 

set xtics border in scale 0,0 nomirror rotate by -90 offset character 0, 0, 0 font "arial,9"
set x2tics ("HEPATITIS-20" 5.0, "CHESS-40" 15.0, "CONNECT-40" 25.0, "HEART-CLEVELAND-20" 35.0, "KR-VS-KP-40" 45.0, "MUSHROOM-5" 55.0, "RETAIL-5" 65.0, "T10I4D100K-5" 75.0, "T40I4D100K-5" 85.0) out nomirror
set x2tics border in scale 0,0 nomirror rotate by 45 offset character 0, 0, 0 font "arial,7"

set key inside right top vertical Left reverse enhanced noautotitles box

set xrange [0.5:91.0]
set x2range [0.5:91.0]
set yrange [1:*]

set style line 1 lt 0 lw 3 linecolor rgb "black"

set arrow from 10.5,1 to 10.5,1e5 nohead ls 1
set arrow from 20.5,1 to 20.5,1e5 nohead ls 1
set arrow from 30.5,1 to 30.5,1e5 nohead ls 1
set arrow from 40.5,1 to 40.5,1e5 nohead ls 1
set arrow from 50.5,1 to 50.5,1e5 nohead ls 1
set arrow from 60.5,1 to 60.5,1e5 nohead ls 1
set arrow from 70.5,1 to 70.5,1e5 nohead ls 1
set arrow from 80.5,1 to 80.5,1e5 nohead ls 1


plot \
"graph/hepatitis/hepatitis_PATTERNS.txt" u 2:4 w lp lw 1 lt 1 pt 3 ps 1.2 t "# patterns - MINCOV",\
"graph/hepatitis/hepatitis_PATTERNS.txt" u 2:5 w lp lw 1 lt 2 pt 6 ps 1.2 t "# patterns - FIRSTWITCOV",\
"graph/hepatitis/hepatitis_PATTERNS.txt" u 2:3 w points pt 9 ps 1.2 t  "# witness patterns ",\
"graph/chess/chess_PATTERNS.txt" u ($2+10):4 w  lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/chess/chess_PATTERNS.txt" u ($2+10):5 w  lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/chess/chess_PATTERNS.txt" u ($2+10):3 w  points pt 9 ps 1.2 notitle,\
"graph/connect/connect_PATTERNS.txt" u ($2+20):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/connect/connect_PATTERNS.txt" u ($2+20):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/connect/connect_PATTERNS.txt" u ($2+20):3 w points pt 9 ps 1.2 notitle,\
"graph/heart-cleveland/heart-cleveland_PATTERNS.txt" u ($2+30):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/heart-cleveland/heart-cleveland_PATTERNS.txt" u ($2+30):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/heart-cleveland/heart-cleveland_PATTERNS.txt" u ($2+30):3 w points pt 9 ps 1.2 notitle,\
"graph/kr-vs-kp/kr-vs-kp_PATTERNS.txt" u ($2+40):4 w  lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/kr-vs-kp/kr-vs-kp_PATTERNS.txt" u ($2+40):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/kr-vs-kp/kr-vs-kp_PATTERNS.txt" u ($2+40):3 w points pt 9 ps 1.2 notitle,\
"graph/mushroom/mushroom_PATTERNS.txt" u ($2+50):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/mushroom/mushroom_PATTERNS.txt" u ($2+50):5 w  lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/mushroom/mushroom_PATTERNS.txt" u ($2+50):3 w  points pt 9 ps 1.2 notitle,\
"graph/retail/retail_PATTERNS.txt" u ($2+60):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/retail/retail_PATTERNS.txt" u ($2+60):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/T10I4D100K/T10I4D100K_PATTERNS.txt" u ($2+70):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/T10I4D100K/T10I4D100K_PATTERNS.txt"u ($2+70):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\
"graph/T40I10D100K/T40I10D100K_PATTERNS.txt" u ($2+80):4 w lp lw 1 lt 1 pt 3 ps 1.2 notitle,\
"graph/T40I10D100K/T40I10D100K_PATTERNS.txt"u ($2+80):5 w lp lw 1 lt 2 pt 6 ps 1.2 notitle,\





