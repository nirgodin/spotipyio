from typing import Dict, Type

from spotipyio.testing.components.artists.artists_info_test_component import ArtistsInfoTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class ArtistsTestManager(BaseTestManager):
    def __init__(self, info: ArtistsInfoTestComponent):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "info": ArtistsInfoTestComponent,
        }
