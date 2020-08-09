from app.entities.builders.EntityBuilder import EntityBuilder
from app.entities.directors.Director import Director
from app.exchange_rates.ExchangeRateFactory import ExchangeRateFactory


class ExchangeRateStateDirector(Director):
    def __init__(
            self,
            assets,
            exchange_rate_factory: ExchangeRateFactory,
            builder: EntityBuilder
    ):
        self.__assets = assets
        self.__exchange_rate_factory = exchange_rate_factory
        self._builder = builder

    def _create(self):
        def create_component_from_asset(asset):
            return asset["name"], self.__exchange_rate_factory.create(
                asset["name"],
                asset["amount"]
            )

        self._builder.set_id("exchange-rate-state")

        for asset in self.__assets:
            self._builder.add_component(
                *create_component_from_asset(asset)
            )

