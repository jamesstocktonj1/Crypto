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

The "Total Return" value generated is simply the sum of all the returns of each trade. The actual value should be higher due to compound interest of all the simultaneous trades. These are very promising results but more data is still needed to try and refine these values.


#### Disclaimer
This code is non-functional and for concept only. Do not use to trade as I will not be responsible for any money lost.
