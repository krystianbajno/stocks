from threading import Thread


class App:
    configuration = {}
    services = {}
    systems = []
    entities = {}

    def add_entity(self, name, entity):
        self.entities[name] = entity

    def add_system(self, function):
        self.systems.append(function(self))

    def register(self, provider):
        provider = provider(self)
        provider.register()

    def configure(self, name, config):
        self.configuration[name] = config

    def config(self):
        return self.configuration

    def bind(self, interface, function):
        self.services[interface] = function(self)

    def make(self, name):
        return self.services[name]

    def run_systems(self, tick):
        def run_system(s):
            while True:
                s.handle(self.entities)
                tick()

        for system in self.systems:
            thread = Thread(target=run_system, args=[system])
            thread.start()
