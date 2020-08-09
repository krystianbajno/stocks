from app.providers.Provider import Provider


class AppEntityProvider(Provider):
    def register(self):
        self.app.add_entity("state", {})
