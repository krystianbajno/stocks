import time

from app.App import App
from app.enum.EntityEnum import EntityEnum
from config.Assets import config as assets_config
from app.providers.AppEntityProvider import AppEntityProvider
from app.providers.AppServiceProvider import AppServiceProvider
from app.providers.AppSystemProvider import AppSystemProvider


def main():
    boot_application = App()

    boot_application.configure("settings", {
        "system_tick": 0.05,
        "should_update": True
    })

    boot_application.configure("assets", assets_config())

    boot_application.register(AppServiceProvider),
    boot_application.register(AppEntityProvider),
    boot_application.register(AppSystemProvider)

    boot_application.boot()

    boot_application.run_systems(
        lambda entities: time.sleep(
            entities[EntityEnum.SETTINGS.value]
                .get_component_by_id("system_tick")
        )
    )


if __name__ == "__main__":
    main()
