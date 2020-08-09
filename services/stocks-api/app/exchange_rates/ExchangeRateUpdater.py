from app.exchange_rates.ExchangeRate import ExchangeRate


class ExchangeRateUpdater:
    def update(
            self,
            exchange_rate: ExchangeRate,
            new_price_bid: float,
            new_price_ask: float
    ):
        exchange_rate.set_value_of_base_asset_in_compared_asset_bid(new_price_bid)
        exchange_rate.set_value_of_base_asset_in_compared_asset_ask(new_price_ask)

