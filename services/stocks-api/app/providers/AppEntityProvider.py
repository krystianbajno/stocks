from app.entities.Entity import Entity
from app.providers.Provider import Provider


class AppEntityProvider(Provider):
    def boot(self):
        exchange_rate_factory = self.app.make("ExchangeRateFactory")

        exchange_rate_state = Entity()
        exchange_rate_state.set_id("exchange-rate-state")

        for asset in self.app.config()["assets"]:
            exchange_rate_state.put_component(
                asset["name"],
                exchange_rate_factory.create(
                    asset["name"],
                    asset["amount"]
                )
            )
        self.app.add_entity(exchange_rate_state)

        settings = Entity()
        settings.set_id("settings")
        settings.put_component("should_update", True)
        self.app.add_entity(settings)

