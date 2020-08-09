class Entity:
    is_alive = True
    id = None
    components = {}

    def set_id(self, identifier: str) -> None:
        self.id = identifier

    def get_id(self) -> str:
        return self.id

    def put_component(self, identifier: str, component: object) -> None:
        self.components[identifier] = component

    def remove_component_by_id(self, identifier: str) -> None:
        self.components.pop(identifier)

    def set_is_alive(self, is_alive: bool) -> None:
        self.is_alive = is_alive

    def get_is_alive(self) -> bool:
        return self.is_alive

    def get_component_by_id(self, identifier: str):
        return self.components[identifier]

    def get_components(self) -> dict:
        return self.components



