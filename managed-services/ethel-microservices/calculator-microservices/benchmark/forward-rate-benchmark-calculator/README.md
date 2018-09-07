# Forward Rate Benchmark Calculator
Benchmark rate calculator for Outright Forwards

# CALCULATION METHOD
The FX Forward market is constantly monitored by capturing rates every 2 minutes and performing continuous and interactive validation. The captured market data is subject to currency specific systematic tolerance checks which identify outlying data. Validation is performed on the outlying data by Operations Specialists, who will seek corroboration, or rely upon their own judgement to determine the market level. On the hour a snapshot of quoted rates is taken for each tenor, and considered the benchmark fix, subject to further currency specific tolerance checks prior to publication.

The use of such judgement may be appropriate to assess the validity of rates throughout this process, with quality control guidelines and procedures governing each application of such judgement.

Once the rates have been validated, premiums and discounts to GBP and EUR are calculated using the outright forward rates; an example of this is under section 6.3. Legacy currency premium/discounts are calculated using the fixed euro conversion rates; an example is shown under section 6.4. Further base currencies may be published, and if so, these will be calculated using the same principles.

All forward rates are published using premiums or discounts that can be directly added to the spot rate to provide an outright forward rate. Note that ON and TN premiums/discounts should be subtracted from the spot rate to calculate an outright forward rate. ISO codes are used.

All forward rates (bid, offer and mid) are rounded to five decimal places after the decimal point. Where a “5” is encountered, the convention is to round up.

## Local Close Currencies
For currencies where offshore trading is not permitted, the forward rates are published in line with local market levels. This means that when local markets are opened, the published forward rates will reflect activity in that market. When the local market closes, the forward rates published in each subsequent fix remain unchanged.

This impacts the following currencies. Please note that the “Open Time” and “Close Fix” for each currency are subject to change.

ISO | OPEN TIME | CLOSE FIX
--- | --- | ---
CNY | 01:15 GMT | 09:00 GMT
IDR/IDT | 01:15 GMT | 09:00 GMT
KRW | 23:15 GMT | 07:00 GMT
MYR | 23:15 GMT | 10:00 GMT
PHP | 00:15 GMT | 08:00 GMT
THB | 00:15 GMT | 10:00 GMT
TWD | 00:15 GMT | 07:00 GMT

The method of fixing the rates is protected by a patent awarded in 2008, US serial 2002–0042765.
Document Version 4
Date of issue: November 2017

##FORWARD RATE PRODUCTS
* Closing Forward Rates
* Historical Forward Rates
* Intraday Forwards Rates
