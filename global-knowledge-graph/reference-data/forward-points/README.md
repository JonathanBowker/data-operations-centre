![Forex Graph](https://github.com/JonathanBowker/fxoc/blob/master/knowledge-graph/images/forex-graph.png)

# PointQuotes

| Label | Description |
| --- | --- |
| CreatedTimestamp | Time the bucket was created |
| RoutingKey | A unique routing key for each bucket made up of timestamp, currency pair, tenor, trading day and bucket number |
| PointsZipLink | Link to a Zip file containing all of de-duplicated the Point events in the bucket |
| PointOpen | Opening Point mid rate of the bucket |
| PointHigh | Highest Point mid rate of the bucket |
| PointLow | Lowest Point mid rate of the bucket |
| PointCloseBid | Closing Point bid rate of the bucket |
| PointCloseAsk | Closing Point ask rate of the bucket |
| PointCloseMid | Closing Point mid rate of the bucket |
| PointCloseSpread | Closing Point spread of the bucket |
| PointQuoteCount | Total number of Point events in the bucket |
| PointChangeCount | Total number of Point quote direction changes for the bucket |
| PointTravelled | Sum of the absolute unique changes of the Point for the bucket |
| PointIncrement | PointTravelled divided by PointQuoteCount |


