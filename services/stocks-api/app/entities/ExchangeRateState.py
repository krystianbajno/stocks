from app.entities.Entity import Entity


class ExchangeRateState(Entity):
    id = "ExchangeRateState"

    def exchange_rates(self):
        return map(
            lambda key: self.get_component_by_id(key),
            self.get_components()
        )
