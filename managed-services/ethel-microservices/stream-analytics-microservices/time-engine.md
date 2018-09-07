## Time Engine

![tim stream logo small_3](https://user-images.githubusercontent.com/1875500/43993209-d9b2eb10-9d81-11e8-8f3e-61c6cb79cf1e.png)

The Time Engine allows for unspecified data sets to be aggregated in real time.
##
The Time Engine supports the following parameters, to allow for the aggregation of data over an unspecified time.
##
* Duration in milliseconds
* Start of Day e.g. 22:00:00.000
* End of Day e.g. 21:59:59.999 (Should we allow end of day to be specified or is it always start of day - 1?)
##
If Start of Days is not midnight then, based on the transaction date, a bucket date will be determined.
##
For example: -
##
If the transaction time is 2018-08-09 09:00:00 and start of day is 22:00:00, then the bucket date for this transaction is 2018-08-08. Is this correct?
