class ExchangeRate:
    def __init__(self):
        self.price_code = None
        self.compared_amount = None
        self.amount = None

    def set_asset_code(self, price_code: str) -> None:
        self.price_code = price_code

    def get_asset_code(self) -> str:
        return self.price_code

    def set_value_of_base_asset_in_compared_asset(self, amount: float) -> None:
        self.amount = amount

    def get_value_of_base_asset_in_compared_asset(self) -> float:
        return self.amount

    def get_amount_of_compared_asset(self):
        return self.compared_amount

    def set_amount_of_compared_asset(self, amount: float) -> None:
        self.compared_amount = amount

    def get_sum_of_owned(self):
        return (self.get_value_of_base_asset_in_compared_asset() * self.get_amount_of_compared_asset()
            if self.get_value_of_base_asset_in_compared_asset() and self.get_amount_of_compared_asset()
            else None
        )
