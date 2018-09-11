# TiQu - High Frequency Spot MidRate Calculations

## Spot Mid-Rate and Spread Calculation
A median for both the bid rates and ask rates are independently calculated over a fixed time period bucket, then added together and divided by 2 to create the spot mid-rate. The bid and offer median rates are also subtracted to calculate the spread. The outright forward bid and offer median rates are also subtracted to calculate the median spread.

## Engine Configuration:

* **Window Size**: 5 milliseconds
* **Input**: All Spot rates CcyPair, Tenor, BidRate, AskRate 
* **Filters**: Exclude OTCV and OTCD sources.
* **Output** - See table below

## OutPut Fields:

| No | Field | Descrip§tion | Calculation |
| -- | -- | -- | -- |
| 1 | CcyPair | Currency pair | (Sum of Bid transactions)/ TransactionCount |
| 2 | Tenor | Tenor = (SP) | Tenor = (SP) |
| 3 | BidRate | The median Bid rate | (Sum of Bid transactions)/ TransactionCount |
| 4 | AskRate | The median Ask rate | (Sum of Ask transactions)/ TransactionCount | 
| 5 | MidRate | The calculated Mid rate | (AskRate)- (BidRate) | 
| 6 | MidRateChange | The change in Spread between the current bucket and the previous bucket | (previous MidRate – current MidRate) |
| 6 | MidRateChange% | The change in Spread between the current bucket and the previous bucket as a % | (previous MidRate – current MidRate) |
| 7| Spread | The Bid-Ask spread | MidBidRate - MidAskRate | 
| 9 | SpreadChange | The change in Spread between the current bucket and the previous bucket | (previous MidSpread – MidSpread) | 
| 8 | SpreadChange% | The change in Spread between the current bucket and the previous bucket as a % | (MidBidRate - MidAskRate)/ MidAskRate | 

