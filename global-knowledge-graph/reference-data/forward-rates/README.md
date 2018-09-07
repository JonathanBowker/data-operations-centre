# FwdQuotes

| Label | Description |
| --- | --- |
| CreatedTimestamp | Time the bucket was created |
| RoutingKey | A unique routing key for each bucket made up of timestamp, currency pair, tenor, trading day and bucket number |
| FwdsZipLink | Link to a Zip file containing all of de-duplicated the Point events in the bucket |
| FwdOpen | Opening Forward mid rate of the bucket |
| FwdHigh | Highest Forward mid rate of the bucket |
| FwdLow | Lowest Forward mid rate of the bucket |
| FwdCloseBid | Closing Forward bid rate of the bucket |
| FwdCloseAsk | Closing Forward ask rate of the bucket |
| FwdCloseMid | Closing Forward mid rate of the bucket |
| FwdCloseSpread | Closing Forward spread of the bucket |
| FwdQuoteCount | Total number of all the Forward events in the bucket |
| FwdChangeCount | Total number of Foward quote direction changes for the bucket |
| FwdTravelled | Sum of the absolute unique changes of the Forward for the bucket |
| FwdIncrement | FwdTravelled divided by PointQuoteCount |


