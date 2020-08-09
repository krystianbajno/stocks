class CoinbaseResponse:
    bid = 0
    ask = 0
    product_id = None

    def set_bid(self, bid):
        self.bid = float(bid)

    def get_bid(self):
        return self.bid

    def set_ask(self, ask):
        self.ask = float(ask)

    def get_ask(self):
        return self.ask

    def get_product_id(self):
        return self.product_id

    def set_product_id(self, product_id):
        self.product_id = product_id

        