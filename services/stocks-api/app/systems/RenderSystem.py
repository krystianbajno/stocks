from app.cli.CliView import CliView
from app.systems.System import System


class RenderSystem(System):
    def __init__(self, state_printer: CliView):
        self.state_printer = state_printer

    def handle(self, entities):
        self.state_printer.render()
