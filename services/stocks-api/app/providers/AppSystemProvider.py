from app.providers.Provider import Provider
from app.systems.ExchangeTablesRefreshSystem import ExchangeTablesRefreshSystem
from app.systems.RenderSystem import RenderSystem
from app.systems.StateAssetsRefreshSystem import StateAssetsRefreshSystem


class AppSystemProvider(Provider):
    def boot(self):
        self.app.add_system(
            lambda app: ExchangeTablesRefreshSystem(
                app.make("AssetTableResolver"),
                app.config()["settings"]["system_tick"]
            )
        )

        self.app.add_system(
            lambda app: StateAssetsRefreshSystem(
                app.make("ExchangeRateUpdater"),
                app.make("AssetTableResolver")
            )
        )

        self.app.add_system(
            lambda app: RenderSystem(app.make("RenderSystem"))
        )
