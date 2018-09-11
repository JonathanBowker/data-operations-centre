# TiQu - High Frequency Spot MidRate (Benchmark)

## Spot Mid-Rate and Spread Calculation
A median for both the bid rates and ask rates are independently calculated over a fixed time period bucket, then added together and divided by 2 to create the spot mid-rate. The bid and offer median rates are also subtracted to calculate the spread. The outright forward bid and offer median rates are also subtracted to calculate the median spread.

## Engine Configuration:

* **Window Size**: 50 milliseconds
* **Input**: All Spot rates CcyPair, Tenor, BidRate, AskRate 
* **Filters**: Exclude OTCV and OTCD sources.
* **Output** - See table below

## OutPut Table:

| No | Field | Description | Calculation |
| -- | -- | -- | -- |
| 1 | CreatedAt | Timeststamp Created | YYYY|mm|DD'T'HH:mm:SS.ZZZ |
| 1 | Record No | 0000001 to 4300000 (over 24 Hours) | 0000001 |
| 2 | TradingDay | YYYYmmDD | 20180101 |
| 3 | CcyPair | Currency pair | BASE/REF |
| 4 | Tenor | Tenor | SP |
| 5 | TransactionCount | Transaction count | Integer |
| 5 | MedianBidRate | The median Bid rate | (Sum of Bid transactions)/ TransactionCount |
| 6 | MedianAskRate | The median Ask rate | (Sum of Ask transactions)/ TransactionCount | 
| 7 | MidRate | The calculated Mid rate | (MedianAskRate) - (MedianBidRate) | 

