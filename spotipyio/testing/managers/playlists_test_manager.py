from typing import Type, Dict

from spotipyio.testing.components import PlaylistsCreatorTestComponent, PlaylistsInfoTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class PlaylistsTestManager(BaseTestManager):
    def __init__(self, info: PlaylistsInfoTestComponent, create: PlaylistsCreatorTestComponent):
        super().__init__()
        self.info = info
        self.create = create

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "info": PlaylistsInfoTestComponent,
            "create": PlaylistsCreatorTestComponent,
        }
