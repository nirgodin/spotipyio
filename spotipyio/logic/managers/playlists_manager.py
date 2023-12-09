from typing import Dict, Type

from spotipyio.contract.base_manager import BaseManager
from spotipyio.contract.collectors.base_collector import BaseCollector
from spotipyio.logic.collectors.singles_collectors.playlists_collector import PlaylistsCollector
from spotipyio.logic.creators.playlists.playlists_creator import PlaylistsCreator


class PlaylistsManager(BaseManager):
    def __init__(self, info: PlaylistsCollector, create: PlaylistsCreator):
        super().__init__()
        self.info = info
        self.create = create

    @staticmethod
    def _components() -> Dict[str, Type[BaseCollector]]:
        return {
            "info": PlaylistsCollector,
            "create": PlaylistsCreator
        }
