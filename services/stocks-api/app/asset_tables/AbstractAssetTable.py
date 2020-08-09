class AbstractAssetTable:
    assets_table = {}

    def update(self):
        pass

    def set_asset_exchange_info_by_code(self, code, bid_value, ask_value):
        self.assets_table[code] = (bid_value, ask_value)

    def get_asset_exchange_info_by_code(self, code):
        return self.assets_table.get(code)

    def resolvable_for(self):
        pass
