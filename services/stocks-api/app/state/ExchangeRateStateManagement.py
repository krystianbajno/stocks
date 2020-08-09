from app.entities.ExchangeRateState import ExchangeRateState
from app.exchange_rates.ExchangeRateUpdater import ExchangeRateUpdater


class ExchangeRateStateManagement:
    def __init__(
            self,
            state: ExchangeRateState,
            exchange_rate_updater: ExchangeRateUpdater
    ):
        self.state = state
        self.exchange_rate_updater = exchange_rate_updater

    def initialize(self, assets):
        for asset in assets:
            self.state.put_component(asset.get_asset_code(), asset)

    def update_asset(self, asset_name, price):
        self.exchange_rate_updater.update_price(
            self.state.get_component_by_id(asset_name),
            price
        )

    def get_asset_names(self):
        return self.state.get_components().keys()
