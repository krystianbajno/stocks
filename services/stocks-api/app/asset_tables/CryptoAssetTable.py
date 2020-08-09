from app.api.CryptoApi import CryptoApi
from app.asset_tables.AbstractAssetTable import AbstractAssetTable


class CryptoAssetTable(AbstractAssetTable):
    def __init__(self, api: CryptoApi):
        self.api = api

    def update(self):
        for product in self.api.get_assets_table():
            asset, bid, ask = product
            self.set_asset_exchange_info_by_code(asset, bid, ask)
    
    def resolvable_for(self):
        return self.api.client.products
