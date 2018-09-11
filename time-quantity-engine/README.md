# Time and Quantity (TiQu) Bucketing and Analysis Engine



| No | Field | Description | Calculation |
| -- | -- | -- | -- |
| 1 | BidRate | The median Bid rate | (Sum of Bid transactions)/ TransactionCount |
| 2 | AskRate | The median Ask rate | (Sum of Ask transactions)/ TransactionCount | 
| 3 | PreviousMidRate | The previous bucket MidRate | Carry forward previous bucket MidRate | 
| 4 | MidRate | The mid-rate between the MidBidRate and the MidAskRate | (MidBidRate + MidAskRate)/2 | 
| 5 | MidRateChange | The change in rate between the current bucket and the previous bucket | (Previous bucket MidChange) – (Current bucket MidChange) | 
| 6 | RateChange% | The MidChange as a percentage | (MidChange / Previous bucket MidChange) x 100 | 
| 7 | PreviousSpread | The previous bucket Spread | MidBidRate - MidAskRate | 
| 8 | Spread | The Bid-Ask spread | MidBidRate - MidAskRate | 
| 9 | Spread% | The MidSpread as a percentage | (MidBidRate - MidAskRate)/ MidAskRate | 
| 10 | SpreadChange | The change in rate between the current bucket and the previous bucket | (previous MidSpread – MidSpread) | 
| 11 | SpreadChange% |The change in rate between the current bucket and the previous bucket as a percentage | (MidSpread / Previous bucket MidSpread) x 100 | 
| 12 | TransactionCount | Number of transaction (quotes) in the bucket | Total Number of Transactions | 
| 13 | ChangeCount | Number of price change transactions (quotes) in the bucket | Total Number of price change transactions in the bucket | 
| 14 | ChangeAmount | Total amount of price change in the bucket | Total Number of price change transactions in the bucket | 
| 15 | PriceDrift | Number of transaction (quotes) in the bucket | ChangeAmount / ChangeCount | 
