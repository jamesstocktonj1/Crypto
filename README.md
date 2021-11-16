## Object Oriented Algorithm

All the progress so far shows that the principals of the algorithm are very good but I needed a way to be able to implement it easier. This is where the object oriented approach comes into play.

This approach allows a basic Algorithm parent class which has all the functions which will be called in the main programs and from this will be created different child classes which can implement different algorithms (in this case SimpleAlgorithm). This allows me to easily swap in and out different trading algorithms and makes development much easier. 

As I get closer and closer to deploying this algorithm, I am thinking about how I can make my design more foolproof. Firstly is to do with memory management as there is a lot of data storred in arrays (e.g. data, MA7, MA25...). Therefore I will make it so the buffer is resized every so often so only the data which is absolutely needed for decision making is kept. The other reason for this is because python has a memory limitation, especially with multiple arrays of large sizes. Therefore if we want this trading algorithm to be running for weeks or possibly month on end, we can't use up an infinite amount of data.

In addition to this I have also started considering how I will log all the data and trades. For the trades I have decided to use a json file to store both the currently active and completed trades. This will store the both the time and price for both the start point and the end point of the trade, along side the percentage return.

### Algorithm Refinement

I have made some crucial changes to the algorithm after analysing my algorithm's performance on a new 42 hour long data file. In this data file there is a huge drop in the Etherium price which my algorithm couldn't handle. It would try to buy on the way down of the drop and therefore would use up all its maximum trades and then dump them when they reach 0.1% return as they are classed as "Long Trades". To mitigate this, I realised that my algorithm was only good when the volatility of the price was of a medium level. The first piece I implemented was a new "Volatility Value" which is the difference between the maximum price and he minimum price, divided by the minimum price over a set time period (in this case 5000 seconds). This would stop the value from buying if there was a huge spike whether thats upwards or downwards. With this, almost all the trades which were made on the downwards slope were eliminated leaving just the numerous small trades made. This also adds an element of safety to my algorithm and helps to mitigate risks, especially if I end up trading real money.

A second piece I implemented was a running average. This in effect the sum of the total data divided by the size. With this I can then make smarter trades including the following. Firstly, only buy if the point is less than 1% above the average (this point can be adjusted) and secondly also look at the area under the graph between the current data point and the running average. This means when a really low point is detected and it stays low, then we should buy.

I also implemented a kind of hierarchy for the rules. Since there are so many rules which have different levels of risk depending on the scope of data they are tracking, the order that these rules are performed in and the checks done of them are both important. I currently have the rules which look at a small time scope (eg MA25 trough and MA99 - MA25 difference threshold) are all only performed when the volatility value is low enough. Then for the rule looking at the area under the running average, since it looks at data over thousands of seconds, this is not checked by the volatility since it is safe enough to be performed.

#### Disclaimer
This code is non-functional and for concept only. Do not use to trade as I will not be responsible for any money lost.
