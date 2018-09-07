## Volume Imbalance Metric (VIM) Engine

![vim 1 5x](https://user-images.githubusercontent.com/1875500/43994123-963d45c0-9d8f-11e8-9b48-0b5c63335ae2.png)

The VIM Engine allows for unspecified data sets to be aggregated in real time by volume.
##
The VIM Engine supports the following parameters, to allow for the aggregation of data over volume.
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
