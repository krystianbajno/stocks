import json
import time
from threading import Thread

from websocket import create_connection, WebSocketConnectionClosedException


class AbstractWebsocketClient(object):
    thread = None
    stop = False
    sub_params = {}
    keep_alive = None

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stop = False
        self.on_open()
        self.thread = Thread(target=_go)
        self.keep_alive = Thread(target=self._keepalive)
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
        self.keep_alive.start()
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
            self.keep_alive.join()

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
