from typing import Type, Dict

from spotipyio.testing.components import PlaylistsCreatorTestComponent, PlaylistsInfoTestComponent, PlaylistItemsAdderTestComponent
from spotipyio.testing.infra import BaseTestManager, BaseTestComponent


class PlaylistsTestManager(BaseTestManager):
    def __init__(self,
                 add_items: PlaylistItemsAdderTestComponent,
                 create: PlaylistsCreatorTestComponent,
                 info: PlaylistsInfoTestComponent):
        super().__init__()
        self.add_items = add_items
        self.create = create
        self.info = info

    @staticmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        return {
            "add_items": PlaylistItemsAdderTestComponent,
            "create": PlaylistsCreatorTestComponent,
            "info": PlaylistsInfoTestComponent,
        }
