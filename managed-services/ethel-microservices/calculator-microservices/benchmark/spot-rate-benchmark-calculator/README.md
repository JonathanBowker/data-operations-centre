# Spot Rate Benchmark Calculator
Benchmark rate calculator for Spots

## CALCULATION METHOD
The FX market is constantly monitored by capturing rates every 15 seconds and performing continuous and interactive validation.

## Non-Trade Currencies
Over a five minute fix period snapshots of the quoted rates are taken from ICE. These are extracted at 15 second intervals from 2 minutes 30 seconds before to 2 minutes 30 seconds after the fix time.

The median bid and offer rates are independently calculated from the individual snapshots for each currency. These bid and offer rates are validated prior to publication, against currency specific thresholds and this may result in expert judgement being applied.

## Traded Rates
Over a five-minute fix period, actual trades executed and bid and offer order rates from the order matching systems are captured every second from 2 minutes 30 seconds before to 2 minutes 30 seconds after the time of the fix. Trading occurs in milliseconds on the trading platforms and therefore not every trade or order is captured, just a sample.

From each data source, a single traded rate will be captured – this will be identified as a bid or offer depending on whether the Trade is a buy or sell. A spread will be applied to the Trade rate to calculate the opposite bid or offer. The spread applied will be determined by the Order rate captured at the same time. All captured Trades will be subjected to validation checks. This may result in some captured data being excluded from the fix calculation.

Valid Trades from all sources captured during the fix period will be “pooled” together. Subject to a minimum number of valid Trades being present within this pool of data – the Trade rates will be used for the fix. A median Trade bid and Trade offer are calculated independently, using data from the single pool of trades across data sources. The mid-rate is calculated from the median Trade bid and Trade offer. A minimum standard spread is applied to the mid-rate to calculate a new bid and offer. These bid, offer and mid rates will be validated prior to publication, against currency specific tolerance thresholds, and this may result in expert judgement being applied.
If there are insufficient valid Trade rates from the pooled data sources, to be used in the fix then Order rates will be used. From each data source, the best bid and best offer rates will be captured simultaneously to the Trade data from each data source. All captured Order rates will be subjected to validation checks. This may result in some captured data being excluded from the fix calculation.

Order rates from different sources will not be pooled together. Using valid Order rates, a median bid and offer are calculated independently, for each data source. The mid-rate is calculated from the median Order bid and Order offer. A minimum standard spread is applied to the mid-rate to calculate a new bid and offer. The bid, offer and mid rates from the data source with the highest valid Orders over the fix period will be selected as the rates for publication. Consequently the data source to be used will be driven by the market. These bid and offer rates will be validated prior to publication, against currency specific tolerance thresholds, and this may result in expert judgement being applied.

In the event that two or more data sources have an equal number of valid Orders, then an average of the mid-rate from these data sources will be used.

In the event that two or more data sources have a single Order only, the most up to date Order rates will be used.

## Standard Spreads
Pre-defined standard spreads are set for each currency at each fix to reflect liquidity at different times of day.
In order to reflect volatile market conditions, if the market dictates wider spreads than the standard spread then this will be represented in the fix – up to a maximum.

## Local Close Currencies
For currencies where offshore trading is not permitted, the spot rates are published in line with local market levels. This means that when local markets are opened, the published spot rates will reflect activity in that market. When the local market closes, the spot rates published in each subsequent fix remain unchanged. This impacts the following currencies. Please note that the “Open Time” and “Close Fix” for each currency are subject to change.

ISO | OPEN TIME | CLOSE FIX
--- | --- | ---
CNY | 01:15 GMT | 09:00 GMT
IDR/IDT | 01:15 GMT | 09:00 GMT
KRW | 23:15 GMT | 07:00 GMT
MYR | 23:15 GMT | 10:00 GMT
PHP | 00:15 GMT | 08:00 GMT
THB | 00:15 GMT | 10:00 GMT
TWD | 00:15 GMT | 07:00 GMT
BRL | 11:00/12:00GMT* | 20:00/21:00GMT*

* Dependent on Local Daylight Saving Time

The method of fixing the rates is protected by a patent awarded in 2008, US serial 09/972,193.

Once the rates have been validated, cross rates to GBP and EUR are calculated. An example of these calculations is included under section 6.1. For currencies where the market convention is for the spot date to be T+1, no adjustment is made and the calculation is performed as if both currencies are T+2. Likewise no adjustment is made in the cross calculation when market holidays are observed in either currency.
Cross rates to further base currencies may be published, and if so, these will be calculated using the same principles.
The validation process used is protected by the patent detailed above.

Certain rates are calculated from other currencies or from proportions of other currencies, for example, XDR (Special Drawing Rights).
All rates are published using standard market quotation conventions. ISO codes are used.

Bid, offer and mid rates are derived. Mid rates are calculated as the arithmetic mean of rounded bid and offer rates. Bid and offer rates are published to four decimal places; the mid rates are published to five decimal places. Where a “5” is encountered, the convention is to round up.

## SPOT RATE PRODUCTS
*  Closing Spot Rates
* Historical Spot Rates
* Intraday Spot Rates
* Tokyo Fix Rates
* 11am UK Intraday Spot Rates
* 2pm CET Intraday Spot Rates
* 12pm EST Intraday Spot Rates (CAD Noon)
