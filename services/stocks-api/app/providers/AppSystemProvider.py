from app.providers.Provider import Provider
from app.systems.PrintStateSystem import PrintStateSystem
from app.systems.StateAssetsRefreshSystem import StateAssetsRefreshSystem


class AppSystemProvider(Provider):
    def register(self):
        self.app.add_system(
            lambda app: StateAssetsRefreshSystem(app.make("StateManagement"), app.make("AssetTableResolver"))
        )

        self.app.add_system(
            lambda app: PrintStateSystem(app.make("StatePrinter"))
        )