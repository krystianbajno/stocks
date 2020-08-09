from app.entities.builders.EntityBuilder import EntityBuilder


class Director(object):
    _builder: EntityBuilder = None

    def _create(self):
        return NotImplemented

    def build(self):
        self._create()
        result = self._builder.get()
        self._builder.flush()
        return result
