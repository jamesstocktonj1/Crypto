## Initial Non-Live Algorithm

The initial concept of the algorithm shows promising using dummy data collected from live [ETH data](https://github.com/jamesstocktonj1/Crypto/blob/graphical-pre-live/dump5.txt). The graphical-pre.live branch shows the beginning steps of building the algorithm and refining the threshold values.

<p align="center"><img src="https://github.com/jamesstocktonj1/Crypto/blob/graphical-pre-live/media/basic_analysis.png"></p>

The algorithm is largly driven by the MA25 line which is the live data integrated to 25 points (25 seconds). When there is a peak or a trough and the difference between MA25 and the MA99 line then a point of interest is marked.

Using this data, I allowed the program to have a maximum of 5 concurrent trades and the following results were plotted onto the graph. This shows fairly promising results in the short 4 hour data I have. 

<p align="center"><img src="https://github.com/jamesstocktonj1/Crypto/blob/graphical-pre-live/media/basic_analysis_wtrades.png"></p>


#### Disclaimer
This code is non-functional and for concept only. Do not use to trade as I will not be responsible for any money lost.
