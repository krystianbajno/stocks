from app.cli.components.Loader import Loader
from app.entities.ExchangeRateState import ExchangeRateState


class StatePrinter:
    def __init__(self, state: ExchangeRateState):
        self.state = state
        self.loader = Loader()

    def __clear(self):
        print("\033[H\033[J")

    def print(self):
        self.__clear()
        self.loader.step()

        for exchange_rate in self.state.exchange_rates():
            print("[ %s ] Name: %s, Owned: %r, Bid: %r, Owned Summary: %r" % (
                self.loader.print(),
                exchange_rate.get_asset_code(),
                exchange_rate.get_amount_of_compared_asset(),
                exchange_rate.get_value_of_base_asset_in_compared_asset(),
                exchange_rate.get_sum_of_owned(),
            ))
