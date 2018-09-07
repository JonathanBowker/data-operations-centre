# IRDQuotes

IRD Quotes are calculated by ((SpotRate-ForwardRate)/NoDaysinTenor) in Tenor*365

| Label | Description |
| --- | --- |
| CreatedTimestamp | Time the bucket was created |
| RoutingKey | A unique routing key for each bucket made up of timestamp, currency pair, tenor, trading day and bucket number |
| IRDsZipLink | Link to a Zip file containing all of de-duplicated the Point events in the bucket |
| IRDOpen | Opening Forward mid rate of the bucket |
| IRDHigh | Highest Forward mid rate of the bucket |
| IRDLow | Lowest IRD mid rate of the bucket |
| IRDCloseBid | Closing IRD bid rate of the bucket |
| IRDCloseAsk | Closing IRD ask rate of the bucket |
| IRDCloseMid | Closing IRD mid rate of the bucket |
| IRDCloseSpread | Closing IRD spread of the bucket |
| IRDQuoteCount | Total number of all the IRD events in the bucket |
| IRDChangeCount | Total number of IRD quote direction changes for the bucket |
| IRDTravelled | Sum of the absolute changes of the IRD for the bucket |
| IRDIncrement | IRDTravelled divided by PointQuoteCount |


