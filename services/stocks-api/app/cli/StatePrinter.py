from app.cli.components.Loader import Loader


class StatePrinter:
    def __init__(self, state: dict):
        self.state = state
        self.loader = Loader()

    def __clear(self):
        print("\033[H\033[J") 

    def print(self):
        self.__clear()
        for key in self.state.keys():
            print("Name: %s, Owned: %r, Bid: %r, Owned Summary: %r" % (
                self.state[key].get_asset_code(),
                self.state[key].get_amount_of_compared_asset(),
                self.state[key].get_value_of_base_asset_in_compared_asset(),
                self.state[key].get_sum_of_owned(),
            ))
        print("\n[ %s ]\n" % (self.loader.print()))
        self.loader.step()