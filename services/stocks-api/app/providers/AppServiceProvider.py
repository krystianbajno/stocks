import requests
from Crypto.Cipher import ARC4

from app.api.CryptoApi import CryptoApi
from app.api.ForexApi import ForexApi
from app.api.clients.coinbase.CoinbaseWebsocketClient import CoinbaseWebsocketClient
from app.asset_tables.AssetTableResolver import AssetTableResolver
from app.asset_tables.CryptoAssetTable import CryptoAssetTable
from app.asset_tables.ForexAssetTable import ForexAssetTable
from app.cli.CliView import CliView
from app.exchange_rates.ExchangeRateFactory import ExchangeRateFactory
from app.exchange_rates.ExchangeRateUpdater import ExchangeRateUpdater
from app.providers.Provider import Provider


class AppServiceProvider(Provider):
    def register(self):
        def bind_forex_api(app):
            return ForexApi(requests, app.make("ForexDecryptor"))

        def bind_coinbase_client(app):
            return CoinbaseWebsocketClient()

        def bind_crypto_api(app):
            return CryptoApi(app.make("CoinbaseClient"))

        def forex_api_decryptor(to_decrypt):
            return ARC4.new(b'aaf6cb4f0ced8a211c2728328597268509ade33040233a11af') \
                .decrypt(bytearray.fromhex(to_decrypt)) \
                .decode("UTF-8")

        self.app.bind("ForexDecryptor", lambda app: forex_api_decryptor)
        self.app.bind("ForexApi", bind_forex_api)
        self.app.bind("CoinbaseClient", bind_coinbase_client)
        self.app.bind("CryptoApi", bind_crypto_api)

        self.app.bind("CryptoAssetTable", lambda app: CryptoAssetTable(app.make("CryptoApi")))
        self.app.bind("ForexAssetTable", lambda app: ForexAssetTable(app.make("ForexApi")))

        self.app.bind("AssetTableResolver", lambda app: AssetTableResolver([
            app.make("CryptoAssetTable"),
            app.make("ForexAssetTable")
        ]))

        self.app.bind("ExchangeRateFactory", lambda app: ExchangeRateFactory())
        self.app.bind("ExchangeRateUpdater", lambda app: ExchangeRateUpdater())

        self.app.bind("RenderSystem", lambda app: CliView(app.entities))