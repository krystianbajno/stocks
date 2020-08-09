import time

from app.App import App
from app.config.Assets import config as assets_config
from app.providers.AppEntityProvider import AppEntityProvider
from app.providers.AppServiceProvider import AppServiceProvider
from app.providers.AppSystemProvider import AppSystemProvider


def main():
    boot_application = App()

    boot_application.configure("assets", assets_config())

    boot_application.register(AppEntityProvider)
    boot_application.register(AppServiceProvider)
    boot_application.register(AppSystemProvider)

    boot_application.run_systems(lambda: time.sleep(0.05))


if __name__ == "__main__":
    main()
