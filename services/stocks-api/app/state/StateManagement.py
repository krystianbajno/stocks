from app.exchange_rates.ExchangeRateUpdater import ExchangeRateUpdater


class StateManagement:
    def __init__(
            self,
            state: dict,
            exchange_rate_updater: ExchangeRateUpdater
    ):
        self.state = state
        self.exchange_rate_updater = exchange_rate_updater

    def initialize(self, assets):
        for asset in assets:
            self.state[asset.get_asset_code()] = asset

    def update_asset(self, asset_name, price):
        self.exchange_rate_updater.update_price(self.state[asset_name], price)

    def get_asset_names(self):
        return self.state.keys()
