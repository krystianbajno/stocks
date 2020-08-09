from app.api.ForexApi import ForexApi
from app.asset_tables.AbstractAssetTable import AbstractAssetTable


class ForexAssetTable(AbstractAssetTable):
    def __init__(self, api: ForexApi):
        self.api = api

    def update(self):
        for asset, bid in self.api.get_assets_table():
            self.set_asset_exchange_info_by_code(asset, bid, None)

    def resolvable_for(self):
        return ["AUD/CAD", "AUD/CHF", "AUD/HKD", "AUD/JPY", "AUD/NZD", "AUD/SGD", "AUD/USD", "CAD/CHF", "CAD/HKD",
                "CAD/JPY", "CAD/SGD", "CHF/HKD", "CHF/JPY", "CHF/ZAR", "EUR/AUD", "EUR/CAD", "EUR/CHF", "EUR/CZK",
                "EUR/DKK", "EUR/GBP", "EUR/HKD", "EUR/HUF", "EUR/JPY", "EUR/NOK", "EUR/NZD", "EUR/PLN", "EUR/SEK",
                "EUR/SGD", "EUR/TRY", "EUR/USD", "EUR/ZAR", "GBP/AUD", "GBP/CAD", "GBP/CHF", "GBP/HKD", "GBP/JPY",
                "GBP/NZD", "GBP/PLN", "GBP/SGD", "GBP/USD", "GBP/ZAR", "HKD/JPY", "NZD/CAD", "NZD/CHF", "NZD/HKD",
                "NZD/JPY", "NZD/SGD", "NZD/USD", "SGD/CHF", "SGD/HKD", "SGD/JPY", "TRY/JPY", "USD/CAD", "USD/CHF",
                "USD/CNH", "USD/CZK", "USD/DKK", "USD/HKD", "USD/HUF", "USD/INR", "USD/JPY", "USD/MXN", "USD/NOK",
                "USD/PLN", "USD/SAR", "USD/SEK", "USD/SGD", "USD/THB", "USD/TRY", "USD/ZAR", "XAG/JPY", "XAG/USD",
                "XAU/JPY", "XAU/USD", "ZAR/JPY"]
