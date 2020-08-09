from app.api.clients.AbstractWebsocketClient import AbstractWebsocketClient
from app.api.clients.coinbase.CoinbaseResponse import CoinbaseResponse


class CoinbaseWebsocketClient(AbstractWebsocketClient):
    responses = []

    def __init__(self):
        self.url = "wss://ws-feed.pro.coinbase.com"
        self.channels = ["ticker"]
        self.products = ["BTC-USD", "ETH-USD", "ETH-EUR", "BTC-EUR", "BCH-USD", "BCH-EUR"]

    def on_open(self):
        self.sub_params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}

    def on_message(self, msg):
        if "product_id" in msg and "best_bid" in msg:
            coinbase_response = CoinbaseResponse()
            coinbase_response.set_bid(msg["best_bid"])
            coinbase_response.set_ask(msg["best_ask"])
            coinbase_response.set_product_id(msg["product_id"])
            self.responses.append(coinbase_response)

    def consume(self):
        responses = self.responses
        self.responses = []
        return responses
