from app.asset_tables.AssetTableResolver import AssetTableResolver
from app.cli.CliView import CliView
from app.enum.EntityEnum import EntityEnum
from app.exchange_rates.ExchangeRateUpdater import ExchangeRateUpdater
from app.providers.Provider import Provider
from app.systems.ExchangeTablesRefreshSystem import ExchangeTablesRefreshSystem
from app.systems.RenderSystem import RenderSystem
from app.systems.StateAssetsRefreshSystem import StateAssetsRefreshSystem


class AppSystemProvider(Provider):
    def boot(self):
        self.app.add_system(
            lambda app: ExchangeTablesRefreshSystem(
                app.make(AssetTableResolver.__name__),
                app.get_entity_by_id(EntityEnum.SETTINGS.value)
                    .get_component_by_id("system_tick")
            )
        )

        self.app.add_system(
            lambda app: StateAssetsRefreshSystem(
                app.make(ExchangeRateUpdater.__name__),
                app.make(AssetTableResolver.__name__)
            )
        )

        self.app.add_system(
            lambda app: RenderSystem(app.make(CliView.__name__))
        )
