from app.api.CryptoApi import CryptoApi
from app.asset_tables.AbstractAssetTable import AbstractAssetTable


class CryptoAssetTable(AbstractAssetTable):
    def __init__(self, api: CryptoApi):
        self.api = api

    def update(self):
        for product in self.api.get_assets_table():
            asset, bid = product
            self.set_asset_exchange_price_by_code_bid_value(asset, bid)
    
    def resolvable_for(self):
        return self.api.client.products
