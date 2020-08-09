from app.asset_tables.AssetTableResolver import AssetTableResolver
from app.state.StateManagement import StateManagement
from app.systems.System import System


class StateAssetsRefreshSystem(System):
    def __init__(
            self,
            state_management: StateManagement,
            table_resolver: AssetTableResolver
    ):
        self.state_management = state_management
        self.table_resolver = table_resolver

    def handle(self, entity):
        updated_tables = []
        for asset_name in self.state_management.get_asset_names():
            table = self.table_resolver.resolve(asset_name)
            if not table in updated_tables:
                table.update()
                updated_tables.append(table)
            self.state_management.update_asset(asset_name, table.get_asset_exchange_price_by_code(asset_name))
