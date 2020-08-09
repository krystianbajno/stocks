from threading import Thread
from typing import Callable, Any

from app.entities.Entity import Entity
from app.systems.System import System


class App:
    configuration = {}
    providers = []
    services = {}
    systems = []
    entities = {}

    def add_entity(self, function: Callable[[Any], Entity]) -> None:
        entity = function(self)
        self.entities[entity.get_id()] = entity

    def remove_entity(self, label) -> None:
        del self.entities[label]

    def get_entity_by_id(self, identifier) -> Entity:
        return self.entities[identifier]

    def add_system(self, function: Callable[[Any], System]) -> None:
        self.systems.append(function(self))

    def register(self, provider) -> None:
        provider = provider(self)
        provider.register()
        self.providers.append(provider)

    def configure(self, name, config) -> None:
        self.configuration[name] = config

    def config(self) -> dict:
        return self.configuration

    def bind(self, interface, function: Callable) -> None:
        self.services[interface] = function(self)

    def make(self, name):
        return self.services[name]

    def run_systems(self, tick: Callable) -> None:
        def run_system(s):
            while True:
                s.handle(self.entities)
                tick()

        for system in self.systems:
            thread = Thread(target=run_system, args=[system])
            thread.start()

    def boot(self):
        for provider in self.providers:
            provider.boot()
