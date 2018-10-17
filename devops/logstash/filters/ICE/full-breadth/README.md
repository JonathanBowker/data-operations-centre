filter {
  dissect {
    mapping => { "message" => "%{Permission},%{SourceID},%{Type},%{SessionIndicator},%{CurrencyPair},%{TradeType},%{Tenor},%{BidPrice},%{AskPrice},%{ContributorID},%{RegionCode},%{CityCode},%{RegionID},%{CityIDRef},%{CurrentPrice},%{TradeOpen},%{TradeHigh},%{TradeLow},%{Trade Trend},%{TradeTick},%{Change},%{PercentChange},%{TradePrice},%{YesterdayTradeClose},%{TradeDatetime},%{QuoteDatetime},%{ActivityDatetime},%{FractionalIndicator},%{PreviousTradeDate},%{DesktopEligibilityIndicator},%{Refresh%},{midPrice}" }
}
