from app.api.AbstractApi import AbstractAPI
from app.api.clients.coinbase.CoinbaseWebsocketClient import CoinbaseWebsocketClient


class CryptoApi(AbstractAPI):
    def __init__(self, client: CoinbaseWebsocketClient):
        self.client = client
        self.client.start()

    def get_assets_table(self):
        return map(lambda x: (x.get_product_id(), x.get_bid(), x.get_ask()), self.client.consume())
