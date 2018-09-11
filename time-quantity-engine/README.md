# Time and Quantity (TiQu) Bucketing and Analysis Engine

This the process for calculating midrates and analysing buckets of Spot, Outright Forwrads and Interest Rate Differentials at 1 minute intervals:

## Step 1 - Spot Mid-Rate and Spread Calculation
A median for both the bid rates and ask rates are independently calculated over a fixed time period window, then added together and divided by 2 to create the spot mid-rate. The bid and offer median rates are also subtracted to calculate the spread. The outright forward bid and offer median rates are also subtracted to calculate the median spread.

**Input** - _bid, ask spot rates excluding contributions from OTCD and OTCV (OTCX is required becuase is provides calculated spot rates for the cross currencies)_

**Output** - See table below

## Step 2 - Forward Point Mid-Rate and Spread Calculation
A median for both the bid forward points and offer forward points are independently calculated over a fixed time period window, then added together and divided by 2 to create the forward point mid for each currency pair and tenor. 

**Input** - _bid, ask forward point "carry rates" excluding contributions from OTCD and OTCV (OTCX is required becuase is provides calculated spot rates for the cross currencies)_

**Output** - These are only held for calculation of the Outright Forwards in Step -3 

## Step 3 - Outright Forward Mid-Rate and Spread Calculation
For each currency pair and tenor, the forward point bid and ask medians are added to or subtracted from the corresponding spot bid and ask rate medians (by timestamp) to calculate the outright forward ask and bid rates. The outright forward ask and bid rates are then added together and divided by 2 to create the outright forward mid for each currency pair and tenor. The outright forward bid and offer median rates are also subtracted to calculate the median spread.

**Input** - _spot bid, ask spot mid rates form Step 1 and outright forward ask and bid rates from Step 3_

**Output** - See table below

## Step 4 - Interest Rate Differential Mid-Rate and Spread Calculation
For each currency pair and tenor, the outright forward rate bid and ask medians are divided by the corresponding spot (by timestamp) and then annualised before subtracting 1 to calculate the interest rate differential.

**Input** - _outright forward bid and ask rates from Step 3 and the spot bid, ask spot mid rates from Step 1_

**Output** - See table below

# Additional Bucket Calculations
## Step 5 - Price Change and Direction Velocity Calculation
Each window for Spot, Outright Forward and Interest Rate Differentials is analysed for price change and direction velocity. Price change is calculated by subtracting the current window mid from the previous window mid, and the direction velocity is measured by the sum of the amount changed divided by the number of price changes in each window.

## Step 6 - Price Volatility Calculation
Each window for Spot, Outright Forward and Interest Rate Differentials is analysed for opening, high, low and close prices as well as the number of price changes (ChangeCount) in each window. 

* **Input 1 - Spots** - _Spot rates from Step 1_
* **Input 2 - Outright Forwards** - _Outright forward rates from Step 3_
* **Input 3 - Interest Rate Differentials** - _Interest Rate Differentials from Step 4_

**Output** - See table below


| No | Field | Description | Calculation |
| -- | -- | -- | -- |
| 1 | BidRate | The median Bid rate | (Sum of Bid transactions)/ TransactionCount |
| 2 | AskRate | The median Ask rate | (Sum of Ask transactions)/ TransactionCount | 
| 3 | PreviousMidRate | The previous bucket MidRate | Carry forward previous bucket MidRate | 
| 4 | MidRate | The MidRate between the MidBidRate and the MidAskRate | (MidBidRate + MidAskRate)/2 | 
| 5 | MidRateChange | The change in rate between the current bucket and the previous bucket | (Previous bucket MidChange) – (Current bucket MidChange) | 
| 6 | RateChange% | The MidChange as a percentage | (MidChange / Previous bucket MidChange) x 100 | 
| 7 | PreviousSpread | The previous bucket Spread | MidBidRate - MidAskRate | 
| 8 | Spread | The Bid-Ask spread | MidBidRate - MidAskRate | 
| 9 | Spread% | The MidSpread as a percentage | (MidBidRate - MidAskRate)/ MidAskRate | 
| 10 | SpreadChange | The change in MidRate between the current bucket and the previous bucket | (previous MidSpread – MidSpread) | 
| 11 | SpreadChange% |The change in MidRate between the current bucket and the previous bucket as a percentage | (MidSpread / Previous bucket MidSpread) x 100 | 
| 12 | TransactionCount | Number of transaction (quotes) in the bucket | Total Number of Transactions | 
| 13 | ChangeCount | Number of price change transactions (quotes) in the bucket | Total Number of price change transactions in the bucket | 
| 14 | ChangeAmount | Total amount of price change in the bucket | Total Number of price change transactions in the bucket | 
| 15 | PriceDrift | Number of transaction (quotes) in the bucket | ChangeAmount / ChangeCount | 
| 16 | CloseBid | Closing Bid rate | Closing transaction Bid rate | 
| 17 | CloseAsk | Closing Bid rate | Closing transaction Bid rate | 
| 18 | CloseMid | Closing Bid rate | Closing transaction Bid rate | 
| 19 | Open | Opening  Mid rate | Opening transaction Bid rate | 
| 20 | High | Highest Mid rate | Highest Mid rate in the bucket | 
| 21 | Low | Lowest Mid rate | Lowest Mid rate in the bucket | 
