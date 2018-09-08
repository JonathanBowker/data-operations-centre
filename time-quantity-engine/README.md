# Time and Quantity (TiQu) Bucketing and Analysis Engine


| No | Field | Description | Calculation |
| -- | -- | -- | -- |
| 1 | ActualBidRate | The median Bid rate | (Sum of Bid transactions)/ TransactionCount |
| 2 | ActualAskRate | The median Ask rate | (Sum of Ask transactions)/ TransactionCount | 
| 3 | PreviousActualRate | The previous bucket ActualRate | Carry forward previous bucket ActualRate | 
| 4 | ActualRate | The mid-rate between the ActualBidRate and the ActualAskRate | (ActualBidRate + ActualAskRate)/2 | 
| 5 | ActualRateChange | The change in rate between the current bucket and the previous bucket | (Previous bucket ActualChange) – (Current bucket ActualChange) | 
| 6 | RateChange% | The ActualChange as a percentage | (ActualChange / Previous bucket ActualChange) x 100 | 
| 7 | PreviousSpread | The previous bucket Spread | ActualBidRate - ActualAskRate | 
| 8 | Spread | The Bid-Ask spread | ActualBidRate - ActualAskRate | 
| 9 | Spread% | The ActualSpread as a percentage | (ActualBidRate - ActualAskRate)/ ActualAskRate | 
| 10 | SpreadChange | The change in rate between the current bucket and the previous bucket | (previous ActualSpread – ActualSpread) | 
| 11 | SpreadChange% | (ActualSpread / Previous bucket ActualSpread) x 100 | 
| 12 | TransactionCount | Number of transaction (quotes) in the bucket | Total Number of Transactions | 
| 13 | ChangeCount | Number of price change transactions (quotes) in the bucket | Total Number of price change transactions in the bucket | 
| 14 | ChangeAmount | Total amount of price change in the bucket | Total Number of price change transactions in the bucket | 
| 15 | PriceDrift | Number of transaction (quotes) in the bucket | ChangeAmount / ChangeCount | 
