# stock-news-monitoring
This python program will pull the stock prices of stocks we are interested in using API to get this data. 
For example if we are monitoring Tesla stock, it will pull in its price at market close.

Next thing this program will do is pull in its price on the previous day. 
And compare the two prices to get the difference and difference percentage.

Whenever the difference is more than 5%, the API will fetch some relevant news, 
so we can figure out the reason for this rise or fall which will be an indicator on how well this company will do.


Once stock price have triggered this alert then we will send ourselves a message on phone telling what big fluctuation happened and what is the relevant news. 
Using this info we can decide if we want to sell our stock or buy more
