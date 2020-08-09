import time
from threading import Thread
from typing import Callable

from app.entities.Entity import Entity


class App:
    configuration = {}
    providers = []
    services = {}
    systems = []
    entities = {}

    def add_entity(self, entity: Entity) -> None:
        self.entities[entity.get_id()] = entity

    def get_entity_by_id(self, identifier):
        return self.entities[identifier]

    def add_system(self, function: Callable) -> None:
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

    def __run_systems(self, tick: Callable) -> None:
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

        self.__run_systems(
            lambda: time.sleep(self.configuration["system"]["system_tick"])
        )
