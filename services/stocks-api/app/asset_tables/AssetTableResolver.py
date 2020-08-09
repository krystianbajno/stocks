from app.asset_tables.AbstractAssetTable import AbstractAssetTable


class AssetTableResolver:
    def __init__(self, tables):
        self.tables = tables

    def resolve(self, asset_name) -> AbstractAssetTable:
        for table in self.tables:
            if asset_name in table.resolvable_for():
                return table
