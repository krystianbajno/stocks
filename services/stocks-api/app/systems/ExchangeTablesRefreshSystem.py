import time
from threading import Thread

from app.asset_tables.AssetTableResolver import AssetTableResolver


class ExchangeTablesRefreshSystem:
    def __init__(self, table_resolver: AssetTableResolver, thread_sleep):
        self.is_threaded = False
        self.thread_sleep = thread_sleep
        self.table_resolver = table_resolver

    def handle(self, entities):
        if self.is_threaded:
            return

        def handle_thread(tab):
            while True:
                if entities["settings"].get_component_by_id("should_update"):
                    tab.update()
                time.sleep(self.thread_sleep)

        for table in self.table_resolver.tables:
            thread = Thread(target=handle_thread, args=[table])
            thread.start()

        self.is_threaded = True
