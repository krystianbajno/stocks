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

        for key in self.state.get_components():
            asset = self.state.get_component_by_id(key)
            print("[ %s ] Name: %s, Owned: %r, Bid: %r, Owned Summary: %r" % (
                self.loader.print(),
                asset.get_asset_code(),
                asset.get_amount_of_compared_asset(),
                asset.get_value_of_base_asset_in_compared_asset(),
                asset.get_sum_of_owned(),
            ))
