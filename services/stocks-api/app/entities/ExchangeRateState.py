from app.entities.Entity import Entity


class ExchangeRateState(Entity):
    id = "ExchangeRateState"

    def exchange_rates(self):
        return map(
            lambda key: self.components[key],
            self.components
        )
