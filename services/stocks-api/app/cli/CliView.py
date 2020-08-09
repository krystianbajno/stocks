from app.cli.components.Loader import Loader
from app.enum.EntityEnum import EntityEnum


class CliView:
    def __init__(self):
        self.loader = Loader()

    def __clear(self):
        print("\033[H\033[J")

    def render(self, props):
        self.__clear()
        self.loader.step()

        for exchange_rate in props[EntityEnum.EXCHANGE_RATE_STATE.value].get_components().values():
            print("[ %s ] Name: %s, Bid: %r, Ask: %r, Owned: %r, Owned Bid: %r" % (
                self.loader.print(),
                exchange_rate.get_asset_code(),
                exchange_rate.get_value_of_base_asset_in_compared_asset_bid(),
                exchange_rate.get_value_of_base_asset_in_compared_asset_ask(),
                exchange_rate.get_amount_of_compared_asset(),
                exchange_rate.get_sum_of_owned(),
            ))

        print("Should update: " + str(props[EntityEnum.SETTINGS.value].get_component_by_id("should_update")))
