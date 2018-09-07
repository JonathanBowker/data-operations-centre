# SwapPointsQuotes

| Label | Description |
| --- | --- |
| CreatedTimestamp | Time the bucket was created |
| RoutingKey | A unique routing key for each bucket made up of timestamp, currency pair, tenor, trading day and bucket number |
| SwapPointsZipLink | Link to a Zip file containing all of de-duplicated the Point events in the bucket |
| SwapPointOpen | Opening Swap Point mid rate of the bucket |
| SwapPointHigh | Highest Swap Point mid rate of the bucket |
| SwapPointLow | Lowest Swap Point mid rate of the bucket |
| SwapPointCloseBid | Closing Swap Point bid rate of the bucket |
| SwapPointCloseAsk | Closing Swap Point ask rate of the bucket |
| SwapPointCloseMid | Closing Swap Point mid rate of the bucket |
| SwapPointCloseSpread | Closing Swap Point spread of the bucket |
| SwapPointQuoteCount | Total number of all the Swap Point events in the bucket |
| SwapPointChangeCount | Total number of Swap Point quote direction changes for the bucket |
| SwapPointTravelled | Sum of the absolute unique changes of the Swap Points travelled for the bucket |
| SwapPointIncrement | SwapPointTravelled divided by SwapPointQuoteCount |


