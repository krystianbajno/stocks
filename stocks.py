#!/usr/bin/python

import requests
import sys
from time import sleep
import time
from Crypto.Cipher import ARC4
from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException
import json


class AbstractAPI:
    def fetchAssetsTable(self):
        pass

class AbstractWebsocketClient(object):
    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stop = False
        self.on_open()
        self.thread = Thread(target=_go)
        self.keepalive = Thread(target=self._keepalive)
        self.thread.start()

    def _connect(self):
        if self.url[-1] == "/":
            self.url = self.url[:-1]
     
        self.ws = create_connection(self.url)
        self.ws.send(json.dumps(self.sub_params))

    def _keepalive(self, interval=30):
        while self.ws.connected:
            self.ws.ping("keepalive")
            time.sleep(interval)

    def _listen(self):
        self.keepalive.start()
        while not self.stop:
            try:
                data = self.ws.recv()
                msg = json.loads(data)
            except ValueError as e:
                self.on_error(e)
            except Exception as e:
                self.on_error(e)
            else:
                self.on_message(msg)

    def _disconnect(self):
        try:
            if self.ws:
                self.ws.close()
        except WebSocketConnectionClosedException as e:
            pass
        finally:
            self.keepalive.join()

        self.on_close()

    def close(self):
        self.stop = True  
        self._disconnect()
        self.thread.join()

    def on_open(self):
       pass

    def on_close(self):
       pass

    def on_message(self, msg):
       pass

    def on_error(self, e, data=None):
       pass

class CoinbaseResponse:
    bid = 0
    product_id = None

    def setBid(self, bid):
        self.bid = float(bid)

    def getBid(self):
        return self.bid

    def getProductId(self):
        return self.product_id

    def setProductId(self, product_id):
        self.product_id = product_id

class CoinbaseClient(AbstractWebsocketClient):
    responses = []

    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com"
        self.channels = ["ticker"]
        self.products = ["BTC-USD", "ETH-USD", "ETH-EUR", "BTC-EUR", "BCH-USD", "BCH-EUR"]
        self.sub_params = {'type': 'subscribe', 'product_ids': self.products, 'channels': self.channels}

    def on_message(self, msg):
        if "product_id" in msg and "best_bid" in msg:
            coinbase_response = CoinbaseResponse()
            coinbase_response.setBid(msg["best_bid"])
            coinbase_response.setProductId(msg["product_id"])
            self.responses.append(coinbase_response)

    def consume(self):
        responses = self.responses
        self.responses = []
        return responses

class CryptoApi(AbstractAPI):
    def __init__(self, client: CoinbaseClient):
        self.client = client
        self.client.start()

    def getAssetsTable(self):
        return map(lambda x: (x.getProductId(), x.getBid()), self.client.consume())
            
class ForexApi(AbstractAPI):
    def __init__(self, client: requests, decryptor):
        self.client = client
        self.decryptor = decryptor

    def getAssetsTable(self):
        def unpackAssetLine(line):
            asset, bid = line.split('=')[:2]
            bid = float(bid)
            return (asset, bid)

        response = self.decryptor(self.client.get('https://www.oanda.com/lfr/rates_lrrr?tstamp='+str(int(time.time()))).text)
        return map(unpackAssetLine, response.split('\n'))

class AbstractAssetTable:
    assetsTable = {}
    def setAssetExchangePriceByCodeBidValue(self, code, bid_value):
        self.assetsTable[code] = bid_value

    def getAssetExchangePriceByCode(self, code):
        return self.assetsTable.get(code)

    def resolvableFor(self):
        pass

class CryptoAssetTable(AbstractAssetTable):
    def __init__(self, api: CryptoApi):
        self.api = api

    def update(self):
        for product in self.api.getAssetsTable():
            asset, bid = product
            self.setAssetExchangePriceByCodeBidValue(asset, bid)
    
    def resolvableFor(self):
        return self.api.client.products

class ForexAssetTable(AbstractAssetTable):
    def __init__(self, api: ForexApi):
        self.api = api

    def update(self):
        for asset, bid in self.api.getAssetsTable():
            self.setAssetExchangePriceByCodeBidValue(asset, bid)
        
    def resolvableFor(self):
        return ["AUD/CAD","AUD/CHF","AUD/HKD","AUD/JPY","AUD/NZD","AUD/SGD","AUD/USD","CAD/CHF","CAD/HKD","CAD/JPY","CAD/SGD","CHF/HKD","CHF/JPY","CHF/ZAR","EUR/AUD","EUR/CAD","EUR/CHF","EUR/CZK","EUR/DKK","EUR/GBP","EUR/HKD","EUR/HUF","EUR/JPY","EUR/NOK","EUR/NZD","EUR/PLN","EUR/SEK","EUR/SGD","EUR/TRY","EUR/USD","EUR/ZAR","GBP/AUD","GBP/CAD","GBP/CHF","GBP/HKD","GBP/JPY","GBP/NZD","GBP/PLN","GBP/SGD","GBP/USD","GBP/ZAR","HKD/JPY","NZD/CAD","NZD/CHF","NZD/HKD","NZD/JPY","NZD/SGD","NZD/USD","SGD/CHF","SGD/HKD","SGD/JPY","TRY/JPY","USD/CAD","USD/CHF","USD/CNH","USD/CZK","USD/DKK","USD/HKD","USD/HUF","USD/INR","USD/JPY","USD/MXN","USD/NOK","USD/PLN","USD/SAR","USD/SEK","USD/SGD","USD/THB","USD/TRY","USD/ZAR","XAG/JPY","XAG/USD","XAU/JPY","XAU/USD","ZAR/JPY"]

class ExchangeRate:
    def __init__(self):
        self.price_code = None
        self.compared_amount = None
        self.amount = None

    def setAssetCode(self, price_code: str) -> None:
        self.price_code = price_code

    def getAssetCode(self) -> str:
        return self.price_code

    def setValueOfBaseAssetInComparedAsset(self, amount: float) -> None:
        self.amount = amount

    def getValueOfBaseAssetInComparedAsset(self) -> float:
        return self.amount

    def getAmountOfComparedAsset(self) -> None:
        return self.compared_amount

    def setAmountOfComparedAsset(self, amount: float) -> None:
        self.compared_amount = amount    

    def getSumOfOwned(self):
        return (self.getValueOfBaseAssetInComparedAsset() * self.getAmountOfComparedAsset() 
            if self.getValueOfBaseAssetInComparedAsset() and self.getAmountOfComparedAsset() 
            else None
        )
    
class ExchangeRateFactory:
    def create(self, asset_code: str, compared_asset_amount: float):
        exchange_rate = ExchangeRate()
        exchange_rate.setValueOfBaseAssetInComparedAsset(None)
        exchange_rate.setAmountOfComparedAsset(compared_asset_amount)
        exchange_rate.setAssetCode(asset_code)
        return exchange_rate

class ExchangeRateUpdater:
    def updateExchangeRatePrice(
        self,
        exchange_rate: ExchangeRate,
        new_price: float
    ) :
       exchange_rate.setValueOfBaseAssetInComparedAsset(new_price)
        
class StateManagement:
    def __init__(
        self,
        state: dict,
        exchange_rate_updater: ExchangeRateUpdater
    ) :
        self.state = state
        self.exchange_rate_updater = exchange_rate_updater

    def initialize(self, assets):
        for asset in assets:
            self.state[asset.getAssetCode()] = asset
        
    def updateAsset(self, assetName, price):
        self.exchange_rate_updater.updateExchangeRatePrice(self.state[assetName], price)

    def getAssetNames(self):  
        return self.state.keys()

class Loader:
    def __init__(self):
        self.patterns = ["-","/","|","\\"]
        self.st = 0

    def __add(self):
        self.st = self.st + 1

    def __subtract(self):
        self.st = 0

    def step(self):
        if(self.st >= len(self.patterns) - 1):
            self.__anim = self.__subtract
        elif(self.st == 0):
            self.__anim = self.__add    

        self.__anim()

    def print(self):
       return self.patterns[self.st]

class StatePrinter:
    def __init__(self, state: dict):
        self.state = state
        self.loader = Loader()

    def __clear(self):
        print("\033[H\033[J") 

    def print(self):
        self.__clear()
        for key in self.state.keys():
            print("Name: %s, Owned: %r, Bid: %r, Owned Summary: %r" % (
                self.state[key].getAssetCode(),
                self.state[key].getAmountOfComparedAsset(),
                self.state[key].getValueOfBaseAssetInComparedAsset(),
                self.state[key].getSumOfOwned(),
            ))
        print("\n[ %s ]\n" % (self.loader.print()))
        self.loader.step()
        

class AssetTableResolver:
    def __init__(self, tables):
        self.tables = tables

    def resolve(self, assetName):
        for table in self.tables:
            if assetName in table.resolvableFor():
                return table 

class App:
    configuration = {}
    services = {}
    systems = []
    entities = {}

    def addEntity(self, name, entity):
        self.entities[name] = entity

    def addSystem(self, function):
        self.systems.append(function(self))

    def register(self, module, class_name):
        class_ = getattr(module, class_name)
        provider = class_(self)
        provider.register()

    def configure(self, name, config):
        self.configuration[name] = config

    def config(self):
        return self.configuration
        
    def bind(self, interface, function):
        self.services[interface] = function(self)

    def make(self, name):
        return self.services[name]

    def run_systems(self, tick):
        def run_system(system):
            while True:
                system.handle(self.entities)
                tick()
                
        for system in self.systems:
            thread = Thread(target=run_system, args=[system])
            thread.start()

class Provider:
    def __init__(self, app: App):
        self.app = app

    def register(self):
        pass

class AppEntityProvider(Provider):
    def register(self):
        self.app.addEntity("state", {})

class AppSystemProvider(Provider):
    def register(self):
        self.app.addSystem(
            lambda app: StateManagementSystem(app.make("StateManagement"), app.make("AssetTableResolver"))
        )

        self.app.addSystem(
            lambda app: PrintStateSystem(app.make("StatePrinter"))
        )

class AppServiceProvider(Provider):
    def register(self):
        def bindForexApi(app):
            return ForexApi(requests, app.make("ForexDecryptor"))
        
        def bindCoinbaseClient(app):
            return CoinbaseClient()

        def bindCryptoApi(app):
            return CryptoApi(app.make("CoinbaseClient"))

        def bindStateManagement(app):
            exchange_rate_factory = app.make("ExchangeRateFactory")
            instance = StateManagement(app.entities["state"], app.make("ExchangeRateUpdater"))
            instance.initialize(map(lambda entity: exchange_rate_factory.create(entity["name"], entity["amount"]), app.config()["assets"]))
            return instance

        self.app.bind("ForexDecryptor", lambda app: lambda x: ARC4.new(b'aaf6cb4f0ced8a211c2728328597268509ade33040233a11af').decrypt(bytearray.fromhex(x)).decode("UTF-8"))
        self.app.bind("ForexApi", bindForexApi)
        self.app.bind("CoinbaseClient", bindCoinbaseClient)
        self.app.bind("CryptoApi", bindCryptoApi)

        self.app.bind("CryptoAssetTable", lambda app: CryptoAssetTable(app.make("CryptoApi")))
        self.app.bind("ForexAssetTable", lambda app: ForexAssetTable(app.make("ForexApi")))
        self.app.bind("AssetTableResolver", lambda app: AssetTableResolver([
            app.make("CryptoAssetTable"),
            app.make("ForexAssetTable")
        ]))

        self.app.bind("ExchangeRateFactory", lambda app: ExchangeRateFactory())
        self.app.bind("ExchangeRateUpdater", lambda app: ExchangeRateUpdater())

        self.app.bind("StatePrinter", lambda app: StatePrinter(app.entities["state"]))
        self.app.bind("StateManagement", bindStateManagement)


class System:
    def handle(self, entity):
        pass

class StateManagementSystem(System):
    def __init__(
        self,
        state_management,
        table_resolver
    ) :
        self.state_management = state_management
        self.table_resolver = table_resolver

    def handle(self, entity):
        updated_tables = []
        for assetName in self.state_management.getAssetNames():
            table = self.table_resolver.resolve(assetName)
            if not table in updated_tables:
                table.update()
                updated_tables.append(table)
            self.state_management.updateAsset(assetName, table.getAssetExchangePriceByCode(assetName))
        updated_tables = []

class PrintStateSystem(System):
    def __init__(self, state_printer):
        self.state_printer = state_printer

    def handle(self, entities):
        self.state_printer.print()
        
        
def assets_configuration():
    return [
        {"name": "EUR/PLN", "amount":1024},
        {"name": "USD/PLN", "amount":1024},
        {"name": "GBP/PLN", "amount":1024},
        {"name": "EUR/USD", "amount":0},
        {"name": "BTC-USD", "amount": 0.618},
        {"name": "BCH-USD", "amount": 0.618},
        {"name": "ETH-USD", "amount": 0.618},
        {"name": "BTC-EUR", "amount": 0.618},
        {"name": "BCH-EUR", "amount": 0.618},
        {"name": "ETH-EUR", "amount": 0.618}
    ]

def main():
    boot_application = App()

    boot_application.configure("assets", assets_configuration())

    boot_application.register(__import__(__name__), "AppEntityProvider")
    boot_application.register(__import__(__name__), "AppServiceProvider")
    boot_application.register(__import__(__name__), "AppSystemProvider")

    boot_application.run_systems(lambda: time.sleep(0.05))

if __name__ == "__main__":
    main()