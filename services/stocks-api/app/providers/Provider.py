from app.App import App


class Provider:
    def __init__(self, app: App):
        self.app = app

    def register(self):
        pass

    def boot(self):
        pass
