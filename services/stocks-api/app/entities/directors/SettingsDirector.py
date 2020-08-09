from app.entities.builders.EntityBuilder import EntityBuilder
from app.entities.directors.Director import Director
from app.enum.EntityEnum import EntityEnum


class SettingsDirector(Director):
    def __init__(self, builder: EntityBuilder, config: dict):
        self.__config = config
        self._builder = builder

    def _create(self) -> None:
        self._builder.set_id(EntityEnum.SETTINGS.value)
        self._builder.add_component("should_update", self.__config["should_update"])
        self._builder.add_component("system_tick", self.__config["system_tick"])
