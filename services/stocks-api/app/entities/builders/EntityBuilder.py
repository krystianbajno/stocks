from app.entities.Entity import Entity


class EntityBuilder:
    def __init__(self):
        self.entity = Entity()

    def flush(self):
        self.__init__()

    def set_id(self, identifier: str) -> None:
        self.entity.set_id(identifier)

    def add_component(self, identifier, component) -> None:
        self.entity.put_component(identifier, component)

    def get(self) -> Entity:
        return self.entity
