import time
import requests
from app.api.AbstractApi import AbstractAPI


class ForexApi(AbstractAPI):
    def __init__(self, client: requests, decryptor):
        self.client = client
        self.decryptor = decryptor

    def get_assets_table(self):
        def unpack_asset_line(line):
            asset, bid = line.split('=')[:2]
            bid = float(bid)
            return asset, bid

        response = self.decryptor(
            self.client.get('https://www.oanda.com/lfr/rates_lrrr?tstamp='+str(int(time.time()))).text
        )

        return map(unpack_asset_line, response.split('\n'))
