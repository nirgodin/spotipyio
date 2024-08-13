from typing import Type, Dict

from spotipyio.testing.components import PlaylistsInfoTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class PlaylistsTestManager(BaseTestManager):
    def __init__(self, info: PlaylistsInfoTestComponent):
        super().__init__()
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "info": PlaylistsInfoTestComponent,
        }
