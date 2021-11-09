## Command Line Non-Live Algorithm

Using the proposed trading conditions found in the [master](https://github.com/jamesstocktonj1/Crypto#algorithm-finalisation) readme, I created this branch to develop the command line implementation. The final product will be deployed on a non-graphical server so all the graphical plots will be generated in a seperate program (or potentially a website).

First implementation using the tuned values from [graphical-pre-live](https://github.com/jamesstocktonj1/Crypto/tree/graphical-pre-live) shows promising results from the 4 hour live data file. The data is as followed:

```text
Completed Trades
Trade Complete: Buy 4596.6029   Sell 4606.7866  Return 0.222%
Trade Complete: Buy 4597.9700   Sell 4606.7866  Return 0.192%
Trade Complete: Buy 4597.4673   Sell 4606.7866  Return 0.203%
Trade Complete: Buy 4600.3026   Sell 4608.1317  Return 0.170%
Trade Complete: Buy 4597.4265   Sell 4603.8505  Return 0.140%
Trade Complete: Buy 4606.8847   Sell 4619.7538  Return 0.279%
Trade Complete: Buy 4607.5042   Sell 4619.7538  Return 0.266%
Trade Complete: Buy 4603.7592   Sell 4619.7538  Return 0.347%
Trade Complete: Buy 4607.2580   Sell 4630.8393  Return 0.512%
Trade Complete: Buy 4619.2168   Sell 4630.8393  Return 0.252%
Trade Complete: Buy 4620.8752   Sell 4630.8393  Return 0.216%
Trade Complete: Buy 4608.1373   Sell 4625.3948  Return 0.375%

Open Trades
Buy 4618.9068   Return -0.376%
Buy 4622.7617   Return -0.459%
Buy 4623.2465   Return -0.470%
Buy 4623.1545   Return -0.468%
Buy 4625.2821   Return -0.513%

Return Summary
Total Return 4.172%
Highest Return 0.512%
```
Another dataset shows the following results:
```text
Completed Trades
Trade Complete: Buy 4729.2415   Sell 4734.5739  Return 0.113%
Trade Complete: Buy 4729.8030   Sell 4734.5739  Return 0.101%
Trade Complete: Buy 4729.3644   Sell 4743.2668  Return 0.294%
Trade Complete: Buy 4730.9249   Sell 4743.2668  Return 0.261%
Trade Complete: Buy 4731.2851   Sell 4743.2668  Return 0.253%
Trade Complete: Buy 4729.0458   Sell 4739.1069  Return 0.213%
Trade Complete: Buy 4731.1058   Sell 4747.6510  Return 0.350%
Trade Complete: Buy 4740.8027   Sell 4747.6510  Return 0.144%
Trade Complete: Buy 4737.8224   Sell 4747.6510  Return 0.207%
Trade Complete: Buy 4740.6934   Sell 4750.1482  Return 0.199%
Trade Complete: Buy 4735.2339   Sell 4758.0891  Return 0.483%
Trade Complete: Buy 4748.3085   Sell 4758.0891  Return 0.206%
Trade Complete: Buy 4750.7189   Sell 4758.0891  Return 0.155%
Trade Complete: Buy 4748.4645   Sell 4760.7674  Return 0.259%
Trade Complete: Buy 4751.0280   Sell 4760.7674  Return 0.205%
Trade Complete: Buy 4748.4460   Sell 4760.8497  Return 0.261%
Trade Complete: Buy 4753.1618   Sell 4760.8497  Return 0.162%
Trade Complete: Buy 4754.6065   Sell 4761.6988  Return 0.149%
Trade Complete: Buy 4757.9240   Sell 4771.4011  Return 0.283%
Trade Complete: Buy 4759.4441   Sell 4771.4011  Return 0.251%
Trade Complete: Buy 4757.9027   Sell 4771.4011  Return 0.284%
Trade Complete: Buy 4757.7932   Sell 4772.1734  Return 0.302%
Trade Complete: Buy 4759.6146   Sell 4765.8516  Return 0.131%
Trade Complete: Buy 4766.2599   Sell 4772.3821  Return 0.128%
Trade Complete: Buy 4769.7468   Sell 4779.1046  Return 0.196%
Trade Complete: Buy 4771.4874   Sell 4779.1046  Return 0.160%
Trade Complete: Buy 4773.3186   Sell 4779.1046  Return 0.121%
Trade Complete: Buy 4771.4836   Sell 4778.5662  Return 0.148%

Open Trades
Buy 4769.6398   Return 0.098%
Buy 4779.9671   Return -0.118%
Buy 4780.2626   Return -0.124%
Buy 4781.0955   Return -0.141%
Buy 4778.5601   Return -0.088%

Return Summary
Total Return 7.021%
Highest Return 0.483%
```

The "Total Return" value generated is simply the sum of all the returns of each trade. The actual value should be higher due to compound interest of all the simultaneous trades. These are very promising results but more data is still needed to try and refine these values.

After this I created the [graphics_main](https://github.com/jamesstocktonj1/Crypto/blob/cmd-pre-live/graphics_main.py) which takes the trade file dumped by the command line program and then plots it in matplotlib. This allows the command line to be run on a non-graphical server, and then the files to be copied and then analysed on a graphical computer. This means we can check how the trading algorithm is performing. An example graph generated can be seen below.

<p align="center"><img src="https://github.com/jamesstocktonj1/Crypto/blob/main/media/cmd_graphic_output.png"></p>

#### Disclaimer
This code is non-functional and for concept only. Do not use to trade as I will not be responsible for any money lost.
