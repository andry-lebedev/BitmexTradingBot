# wcaholdings

 
******************************************************************
1. Buy only when all the requirements under are met. Pair is XBT-USD, you can have maximum  of 1 trade at the same time:
    1. Bitcoin delta for last 24 hours is less than 3%.
    2. In last 10 seconds volume in 0.5% from average price into bid price is at least 1 500 000 USD.
    3. In last 10 seconds bid volume in those 0.5% must be 4x higher than volume in 0.2% from average price into ask price.
2. When the requirements are met, set market buy order.
 
After coin is bought immediately set stop-limit order to actual buy price - 0.2% and set sell price to buy price +0.2%, after 10 seconds lower the sell price to buy price +0.1%
******************************************************************
Run mainloop to activate 
