class AbstractAssetTable:
    assets_table = {}

    def set_asset_exchange_price_by_code_bid_value(self, code, bid_value):
        self.assets_table[code] = bid_value

    def get_asset_exchange_price_by_code(self, code):
        return self.assets_table.get(code)

    def resolvable_for(self):
        pass
