from app.App import App
from config.Assets import config as assets_config
from app.providers.AppEntityProvider import AppEntityProvider
from app.providers.AppServiceProvider import AppServiceProvider
from app.providers.AppSystemProvider import AppSystemProvider


def main():
    boot_application = App()

    boot_application.configure("system", {
        "system_tick": 0.05
    })

    boot_application.configure("assets", assets_config())

    boot_application.register(AppServiceProvider),
    boot_application.register(AppEntityProvider),
    boot_application.register(AppSystemProvider)

    boot_application.boot()


if __name__ == "__main__":
    main()
