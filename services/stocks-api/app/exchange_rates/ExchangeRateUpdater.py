from app.entities.ExchangeRate import ExchangeRate


class ExchangeRateUpdater:
    def update_price(
            self,
            exchange_rate: ExchangeRate,
            new_price: float
    ):
        exchange_rate.set_value_of_base_asset_in_compared_asset(new_price)
