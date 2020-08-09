from app.entities.builders.EntityBuilder import EntityBuilder
from app.entities.directors.ExchangeRateStateDirector import ExchangeRateStateDirector
from app.entities.directors.SettingsDirector import SettingsDirector
from app.exchange_rates.ExchangeRateFactory import ExchangeRateFactory
from app.providers.Provider import Provider


class AppEntityProvider(Provider):
    def register(self):
        def register_exchange_rate_state_director(app):
            exchange_rate_factory = app.make(ExchangeRateFactory.__name__)
            entity_builder = app.make(EntityBuilder.__name__)
            return ExchangeRateStateDirector(
                app.config()["assets"],
                exchange_rate_factory,
                entity_builder
            )

        def register_settings_director(app):
            entity_builder = app.make(EntityBuilder.__name__)
            return SettingsDirector(entity_builder, app.config()["settings"])

        self.app.bind(EntityBuilder.__name__, lambda app: EntityBuilder())
        self.app.bind(ExchangeRateStateDirector.__name__, register_exchange_rate_state_director)
        self.app.bind(SettingsDirector.__name__, register_settings_director)

    def boot(self):
        self.app.add_entity(lambda app: app.make(ExchangeRateStateDirector.__name__).build())
        self.app.add_entity(lambda app: app.make(SettingsDirector.__name__).build())
