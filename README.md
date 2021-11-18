## Object Oriented Algorithm

All the progress so far shows that the principals of the algorithm are very good but I needed a way to be able to implement it easier. This is where the object oriented approach comes into play.

This approach allows a basic Algorithm parent class which has all the functions which will be called in the main programs and from this will be created different child classes which can implement different algorithms (in this case SimpleAlgorithm). This allows me to easily swap in and out different trading algorithms and makes development much easier. 

As I get closer and closer to deploying this algorithm, I am thinking about how I can make my design more foolproof. Firstly is to do with memory management as there is a lot of data storred in arrays (e.g. data, MA7, MA25...). Therefore I will make it so the buffer is resized every so often so only the data which is absolutely needed for decision making is kept. The other reason for this is because python has a memory limitation, especially with multiple arrays of large sizes. Therefore if we want this trading algorithm to be running for weeks or possibly month on end, we can't use up an infinite amount of data.

In addition to this I have also started considering how I will log all the data and trades. For the trades I have decided to use a json file to store both the currently active and completed trades. This will store the both the time and price for both the start point and the end point of the trade, along side the percentage return.

### Algorithm Refinement

I have made some crucial changes to the algorithm after analysing my algorithm's performance on a new 42 hour long data file. In this data file there is a huge drop in the Etherium price which my algorithm couldn't handle. It would try to buy on the way down of the drop and therefore would use up all its maximum trades and then dump them when they reach 0.1% return as they are classed as "Long Trades". To mitigate this, I realised that my algorithm was only good when the volatility of the price was of a medium level. The first piece I implemented was a new "Volatility Value" which is the difference between the maximum price and he minimum price, divided by the minimum price over a set time period (in this case 5000 seconds). This would stop the value from buying if there was a huge spike whether thats upwards or downwards. With this, almost all the trades which were made on the downwards slope were eliminated leaving just the numerous small trades made. This also adds an element of safety to my algorithm and helps to mitigate risks, especially if I end up trading real money.

A second piece I implemented was a running average. This in effect the sum of the total data divided by the size. With this I can then make smarter trades including the following. Firstly, only buy if the point is less than 1% above the average (this point can be adjusted) and secondly also look at the area under the graph between the current data point and the running average. This means when a really low point is detected and it stays low, then we should buy.

I also implemented a kind of hierarchy for the rules. Since there are so many rules which have different levels of risk depending on the scope of data they are tracking, the order that these rules are performed in and the checks done of them are both important. I currently have the rules which look at a small time scope (eg MA25 trough and MA99 - MA25 difference threshold) are all only performed when the volatility value is low enough. Then for the rule looking at the area under the running average, since it looks at data over thousands of seconds, this is not checked by the volatility since it is safe enough to be performed.

The performance on the 42 hour data can be seen below.

<p align="center"><img src="https://github.com/jamesstocktonj1/Crypto/blob/main/media/updated_rules.png"></p>


## Algorithm Finalisation

After working with and plotting various data using the Graphical Non-Live Algorithm I have finalised the conditions for trading.
```Text
Buy:
 - when MA25 is at a trough and the difference between MA99 and MA25 is large and also the gradient of MA99 can't be less than a slightly negative slope.
 - when MA7 is at a trough and the difference between MA99 and the current value is large.
 - when MA250 is at a trough.

Sell:
 - when MA25 is at a peak and the difference betweeen MA25 and MA99 is large.
 - when MA7 is at a trough and the difference between the current value and MA99 is large.

Additional:
 - In addition to this there will be a threshold which needs to be met in order to sell with sufficient profit (Binance fees are at 0.04%).
```

## Command Line Non-Live Algorithm

Using the proposed trading conditions listed above, I created the [cmd-pre-live](https://github.com/jamesstocktonj1/Crypto/tree/cmd-pre-live) branch to develop the command line implementation of this algorithm. The final product will be deployed on a non-graphical server so all the graphical plots will be generated in a seperate program (or potentially a website).

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


#### Disclaimer
This code is non-functional and for concept only. Do not use to trade as I will not be responsible for any money lost.
