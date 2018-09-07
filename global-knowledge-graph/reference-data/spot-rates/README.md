![Forex Graph](https://github.com/JonathanBowker/fxoc/blob/master/knowledge-graph/images/forex-graph.png)

# SpotQuotes

| Label | Description |
| --- | --- |
| CreatedTimestamp | Time the bucket was created |
| RoutingKey | A unique routing key for each bucket made up of timestamp, currency pair, tenor, trading day and bucket number |
| SpotsZipLink | Link to a Zip file containing all of de-duplicated the Point events in the bucket |
| SpotOpen | Opening Spot mid rate of the bucket |
| SpotHigh | Highest Spot mid rate of the bucket |
| SpotLow | Lowest Spot mid rate of the bucket |
| SpotCloseBid | Closing Spot bid rate of the bucket |
| SpotCloseAsk | Closing Spot ask rate of the bucket |
| SpotCloseMid | Closing Spot mid rate of the bucket |
| SpotCloseSpread | Closing Spot spread of the bucket |
| SpotQuoteCount | Total number of all the Spot events in the bucket |
| SpotChangeCount | Total number of Spot quote direction changes for the bucket |
| SpotTravelled | Sum of the absolute changes of the Spot for the bucket |
| SpotIncrement | SpotTravelled divided by SpotQuoteCount |


