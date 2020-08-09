from app.exchange_rates.ExchangeRate import ExchangeRate


class ExchangeRateFactory:
    def create(self, asset_code: str, compared_asset_amount: float):
        exchange_rate = ExchangeRate()
        exchange_rate.set_value_of_base_asset_in_compared_asset_bid(None)
        exchange_rate.set_value_of_base_asset_in_compared_asset_ask(None)
        exchange_rate.set_amount_of_compared_asset(compared_asset_amount)
        exchange_rate.set_asset_code(asset_code)
        return exchange_rate
