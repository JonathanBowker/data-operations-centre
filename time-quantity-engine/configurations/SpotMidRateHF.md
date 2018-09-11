# TiQu - High Frequency Spot MidRate Calculations

## Spot Mid-Rate and Spread Calculation
A median for both the bid rates and ask rates are independently calculated over a fixed time period bucket, then added together and divided by 2 to create the spot mid-rate. The bid and offer median rates are also subtracted to calculate the spread. The outright forward bid and offer median rates are also subtracted to calculate the median spread.

## Engine Configuration:

* **Window Size**: 5 milliseconds
* **Input**: All Spot rates excluding - OTCV and OTCD sources.
* **Output** - _See table below_

| No | Field | Descrip§tion | Calculation |
| -- | -- | -- | -- |

| 1 | CcyPair | Currency pair | (Sum of Bid transactions)/ TransactionCount |
| 2 | Tenor | Tenor = (SP) | Tenor = (SP) |
| 3 | BidRate | The median Bid rate | (Sum of Bid transactions)/ TransactionCount |
| 4 | AskRate | The median Ask rate | (Sum of Ask transactions)/ TransactionCount | 
| 5 | MidRate | The calculated Mid rate | (AskRate)- (BidRate) | 
| 6 | PreviousMidRate | The previous bucket MidRate | Carry forward previous bucket MidRate | 
| 7| Spread | The Bid-Ask spread | MidBidRate - MidAskRate | 
| 8 | Spread% | The MidSpread as a percentage | (MidBidRate - MidAskRate)/ MidAskRate | 
| 9 | SpreadChange | The change in MidRate between the current bucket and the previous bucket | (previous MidSpread – MidSpread) | 

