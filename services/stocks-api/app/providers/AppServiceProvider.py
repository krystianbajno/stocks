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
            return CryptoApi(app.make(CoinbaseWebsocketClient.__name__))

        def forex_api_decryptor(to_decrypt):
            return ARC4.new(b'aaf6cb4f0ced8a211c2728328597268509ade33040233a11af') \
                .decrypt(bytearray.fromhex(to_decrypt)) \
                .decode("UTF-8")

        self.app.bind("ForexDecryptor", lambda app: forex_api_decryptor)
        self.app.bind(ForexApi.__name__, bind_forex_api)
        self.app.bind(CoinbaseWebsocketClient.__name__, bind_coinbase_client)
        self.app.bind(CryptoApi.__name__, bind_crypto_api)

        self.app.bind(CryptoAssetTable.__name__, lambda app: CryptoAssetTable(app.make(CryptoApi.__name__)))
        self.app.bind(ForexAssetTable.__name__, lambda app: ForexAssetTable(app.make(ForexApi.__name__)))

        self.app.bind(AssetTableResolver.__name__, lambda app: AssetTableResolver([
            app.make(CryptoAssetTable.__name__),
            app.make(ForexAssetTable.__name__)
        ]))

        self.app.bind(ExchangeRateFactory.__name__, lambda app: ExchangeRateFactory())
        self.app.bind(ExchangeRateUpdater.__name__, lambda app: ExchangeRateUpdater())
        self.app.bind(CliView.__name__, lambda app: CliView())
